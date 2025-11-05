"""Webhook handler for AI Music API events."""

import json
import logging
from typing import Any, Callable

from ..common.exceptions import WebhookError
from ..common.utils import verify_webhook_signature
from .models import WebhookEvent

logger = logging.getLogger(__name__)


class WebhookHandler:
    """Handler for webhook events from AI Music API."""

    def __init__(self, secret: str | None = None) -> None:
        """Initialize webhook handler.

        Args:
            secret: Webhook signing secret for verification
        """
        self.secret = secret
        self._event_handlers: dict[str, list[Callable]] = {}

    def verify_signature(
        self,
        payload: str | dict[str, Any],
        signature: str,
    ) -> bool:
        """Verify webhook signature.

        Args:
            payload: Webhook payload
            signature: Signature from X-Webhook-Signature header

        Returns:
            True if signature is valid

        Raises:
            WebhookError: If secret is not configured
        """
        if not self.secret:
            raise WebhookError("Webhook secret not configured")

        return verify_webhook_signature(payload, signature, self.secret)

    def parse_event(self, payload: dict[str, Any]) -> WebhookEvent:
        """Parse webhook payload into event object.

        Args:
            payload: Raw webhook payload

        Returns:
            Parsed webhook event
        """
        return WebhookEvent(**payload)

    def on(self, event_type: str) -> Callable:
        """Decorator to register event handler.

        Args:
            event_type: Event type to handle

        Returns:
            Decorator function

        Example:
            ```python
            handler = WebhookHandler(secret="my_secret")

            @handler.on("task.completed")
            async def handle_completed(event: WebhookEvent):
                print(f"Task completed: {event.task_id}")
                print(f"Audio URL: {event.audio_url}")

            @handler.on("task.failed")
            async def handle_failed(event: WebhookEvent):
                print(f"Task failed: {event.error}")
            ```
        """

        def decorator(func: Callable) -> Callable:
            if event_type not in self._event_handlers:
                self._event_handlers[event_type] = []
            self._event_handlers[event_type].append(func)
            return func

        return decorator

    async def dispatch(self, event: WebhookEvent) -> None:
        """Dispatch event to registered handlers.

        Args:
            event: Webhook event to dispatch
        """
        handlers = self._event_handlers.get(event.event_type, [])

        if not handlers:
            logger.warning(f"No handlers registered for event: {event.event_type}")
            return

        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as e:
                logger.error(f"Error in webhook handler: {e}", exc_info=True)

    async def handle_request(
        self,
        payload: str | dict[str, Any],
        signature: str | None = None,
    ) -> None:
        """Handle incoming webhook request.

        Args:
            payload: Webhook payload (string or dict)
            signature: Signature header value

        Raises:
            WebhookError: If signature verification fails
        """
        # Verify signature if secret is configured
        if self.secret and signature:
            if not self.verify_signature(payload, signature):
                raise WebhookError("Invalid webhook signature")

        # Parse payload
        if isinstance(payload, str):
            payload_dict = json.loads(payload)
        else:
            payload_dict = payload

        # Parse and dispatch event
        event = self.parse_event(payload_dict)
        await self.dispatch(event)


# Import asyncio here to avoid circular import
import asyncio  # noqa: E402
