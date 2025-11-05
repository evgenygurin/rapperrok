"""Exception classes for AI Music API client."""


class AIMusicAPIError(Exception):
    """Base exception for AI Music API errors."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        """Initialize API error.

        Args:
            message: Error message
            status_code: HTTP status code if applicable
        """
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(AIMusicAPIError):
    """Authentication failed - invalid API key."""

    def __init__(self, message: str = "Invalid API key") -> None:
        """Initialize authentication error."""
        super().__init__(message, status_code=401)


class RateLimitError(AIMusicAPIError):
    """Rate limit exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: int | None = None,
    ) -> None:
        """Initialize rate limit error.

        Args:
            message: Error message
            retry_after: Seconds to wait before retry
        """
        self.retry_after = retry_after
        super().__init__(message, status_code=429)


class InsufficientCreditsError(AIMusicAPIError):
    """Insufficient credits for operation."""

    def __init__(
        self,
        message: str = "Insufficient credits",
        credits_required: int | None = None,
        credits_available: int | None = None,
    ) -> None:
        """Initialize insufficient credits error.

        Args:
            message: Error message
            credits_required: Credits needed for operation
            credits_available: Credits currently available
        """
        self.credits_required = credits_required
        self.credits_available = credits_available
        super().__init__(message, status_code=402)


class InvalidParameterError(AIMusicAPIError):
    """Invalid parameter provided."""

    def __init__(self, message: str, parameter_name: str | None = None) -> None:
        """Initialize invalid parameter error.

        Args:
            message: Error message
            parameter_name: Name of invalid parameter
        """
        self.parameter_name = parameter_name
        super().__init__(message, status_code=400)


class ResourceNotFoundError(AIMusicAPIError):
    """Requested resource not found."""

    def __init__(
        self,
        message: str = "Resource not found",
        resource_id: str | None = None,
    ) -> None:
        """Initialize resource not found error.

        Args:
            message: Error message
            resource_id: ID of missing resource
        """
        self.resource_id = resource_id
        super().__init__(message, status_code=404)


class TaskFailedError(AIMusicAPIError):
    """Music generation task failed."""

    def __init__(
        self,
        message: str,
        task_id: str | None = None,
        error_code: str | None = None,
    ) -> None:
        """Initialize task failed error.

        Args:
            message: Error message
            task_id: ID of failed task
            error_code: API error code
        """
        self.task_id = task_id
        self.error_code = error_code
        super().__init__(message, status_code=500)


class TimeoutError(AIMusicAPIError):
    """Operation timed out."""

    def __init__(
        self,
        message: str = "Operation timed out",
        timeout_seconds: int | None = None,
    ) -> None:
        """Initialize timeout error.

        Args:
            message: Error message
            timeout_seconds: Timeout duration in seconds
        """
        self.timeout_seconds = timeout_seconds
        super().__init__(message, status_code=408)


class ValidationError(AIMusicAPIError):
    """Data validation failed."""

    def __init__(self, message: str, errors: dict[str, list[str]] | None = None) -> None:
        """Initialize validation error.

        Args:
            message: Error message
            errors: Dictionary of field errors
        """
        self.errors = errors or {}
        super().__init__(message, status_code=422)


class NetworkError(AIMusicAPIError):
    """Network communication failed."""

    def __init__(self, message: str, original_error: Exception | None = None) -> None:
        """Initialize network error.

        Args:
            message: Error message
            original_error: Original exception that caused the error
        """
        self.original_error = original_error
        super().__init__(message)


class WebhookError(AIMusicAPIError):
    """Webhook processing error."""

    def __init__(self, message: str) -> None:
        """Initialize webhook error."""
        super().__init__(message)
