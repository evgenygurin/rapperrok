# Credits Management Guide

Learn how to manage and optimize your AI Music API credits with RapperRok.

## Understanding Credits

The AI Music API uses a unified credit system across all models (Suno, Producer, Nuro).

### Credit System

- **Monthly Subscription**: Renews credits each month
- **Extra Credits**: Purchase additional credits anytime
- **Consumption**: Credits deducted per operation
- **Rollover**: Unused credits may or may not rollover (check your plan)

## Checking Credits

### Get Current Balance

```python
async with AIMusicClient() as client:
    credits = await client.get_credits()

    print(f"Available: {credits.available}")
    print(f"Total: {credits.total}")
    print(f"Used: {credits.used}")
    print(f"Percentage used: {(credits.used / credits.total) * 100:.1f}%")
```

**Response:**

```python
Credits(
    available=850,
    total=1000,
    used=150,
    subscription_renewal_date="2024-02-01",
    extra_credits=0
)
```

### Check Before Operations

```python
async def safe_generate(client, description):
    # Check credits first
    credits = await client.get_credits()

    if credits.available < 10:
        print("❌ Insufficient credits for generation (need 10)")
        return None

    # Proceed with generation
    return await client.suno.create_music(
        description=description,
        wait_for_completion=True
    )
```

## Credit Costs by Operation

### Suno V4

| Operation | Credits | Notes |
|-----------|---------|-------|
| Create music | 10 | Per generation |
| Extend music | 10 | Per extension |
| Concat music | 5 | Per concatenation |
| Cover music | 10 | Per cover |
| Stems basic (2 tracks) | 20 | Vocals + instrumental |
| Stems full (12 tracks) | 50 | All instrument tracks |
| Create persona | 50 | One-time per persona |
| Persona music | 10 | Per generation |
| WAV export | 10 | Per conversion |
| MIDI export | 5 | Per export |
| Upload music | 0 | Free |
| Get music status | 0 | Free polling |

### Producer

| Operation | Credits | Notes |
|-----------|---------|-------|
| Create | 10 | New music |
| Extend | 10 | Add duration |
| Cover | 10 | Create cover |
| Replace | 10 | Replace section |
| Variation | 10 | Create variation |
| Swap vocals | 15 | Change vocals only |
| Swap instrumental | 15 | Change backing only |
| Upload | 0 | Free |
| Download | 0 | Free (any format) |

### Nuro

| Operation | Credits | Notes |
|-----------|---------|-------|
| Vocal music (30-240s) | 20 | With vocals |
| Instrumental (30-240s) | 15 | No vocals |
| Get music status | 0 | Free polling |

### Lyrics Generation

| Operation | Credits |
|-----------|---------|
| Generate lyrics | 5 |

## Credit Optimization

### 1. Plan Before Generating

```python
async def plan_generation(descriptions, operation_type="create"):
    credits = await client.get_credits()

    # Calculate required credits
    cost_per_operation = 10  # Adjust based on operation
    total_cost = len(descriptions) * cost_per_operation

    print(f"Required: {total_cost} credits")
    print(f"Available: {credits.available} credits")

    if credits.available < total_cost:
        print(f"❌ Need {total_cost - credits.available} more credits")
        return False

    return True
```

### 2. Batch Operations Efficiently

```python
async def batch_with_credit_check(descriptions):
    """Generate multiple tracks with credit monitoring"""
    credits = await client.get_credits()
    results = []

    for i, desc in enumerate(descriptions):
        # Check credits before each operation
        if credits.available < 10:
            print(f"Stopping at {i}/{len(descriptions)} - out of credits")
            break

        try:
            result = await client.suno.create_music(
                description=desc,
                wait_for_completion=True
            )
            results.append(result)

            # Update credits count
            credits.available -= 10

        except InsufficientCreditsError:
            print(f"Ran out of credits at {i}/{len(descriptions)}")
            break

    return results
```

### 3. Choose Cost-Effective Models

```python
async def cost_effective_generation(description, quality_required="medium"):
    """Choose model based on quality needs"""

    if quality_required == "highest":
        # Suno V4 - 10 credits
        return await client.suno.create_music(description=description)

    elif quality_required == "medium":
        # Producer or Nuro - 10/20 credits, faster
        return await client.producer.create_music(
            description=description,
            operation="create"
        )

    elif quality_required == "fast":
        # Producer - 10 credits, 30 seconds
        return await client.producer.create_music(
            description=description,
            operation="create"
        )
```

### 4. Use Basic Stems Instead of Full

```python
async def optimize_stems(song_id, need_full_control=False):
    if need_full_control:
        # Full stems - 50 credits - for professional mixing
        return await client.suno.stems_full(song_id=song_id)
    else:
        # Basic stems - 20 credits - for simple vocal removal
        return await client.suno.stems_basic(song_id=song_id)
```

### 5. Reuse Uploads

```python
# Upload once
with open("track.mp3", "rb") as f:
    upload = await client.producer.upload_music(f, "track.mp3")

audio_id = upload.audio_id

# Reuse for multiple operations
operations = [
    client.producer.create_music(audio_id=audio_id, operation="variation"),
    client.producer.create_music(audio_id=audio_id, operation="extend"),
    client.producer.create_music(audio_id=audio_id, operation="swap_vocals"),
]

results = await asyncio.gather(*operations)
# 30 credits total vs uploading 3 times
```

## Credit Monitoring

### Track Usage

```python
class CreditTracker:
    def __init__(self, client):
        self.client = client
        self.initial_credits = None
        self.operations = []

    async def start(self):
        credits = await self.client.get_credits()
        self.initial_credits = credits.available

    async def track_operation(self, operation_name, credits_cost):
        self.operations.append({
            "operation": operation_name,
            "cost": credits_cost,
            "timestamp": datetime.now()
        })

    async def report(self):
        current = await self.client.get_credits()
        used = self.initial_credits - current.available

        print(f"Initial credits: {self.initial_credits}")
        print(f"Current credits: {current.available}")
        print(f"Used: {used}")
        print(f"\nOperations:")

        for op in self.operations:
            print(f"  - {op['operation']}: {op['cost']} credits")

# Usage
tracker = CreditTracker(client)
await tracker.start()

result = await client.suno.create_music(...)
await tracker.track_operation("create_music", 10)

await tracker.report()
```

### Set Alerts

```python
async def check_credits_with_alert(threshold=100):
    credits = await client.get_credits()

    if credits.available < threshold:
        print(f"⚠️ Low credits: {credits.available} remaining")
        # Send email/notification
        await send_alert(
            f"Low credits: {credits.available} remaining. "
            f"Consider purchasing more."
        )

    return credits.available
```

## Credit Usage Patterns

### Development vs Production

```python
# Development - use test credits
if os.getenv("ENVIRONMENT") == "development":
    DURATION = 30  # Short clips in dev
    CHECK_CREDITS = False
else:
    # Production - optimize costs
    DURATION = 120  # Full tracks
    CHECK_CREDITS = True

async def generate(description):
    if CHECK_CREDITS:
        credits = await client.get_credits()
        if credits.available < 10:
            raise ValueError("Insufficient credits")

    return await client.suno.create_music(
        description=description,
        duration=DURATION,
        wait_for_completion=True
    )
```

### Budget Management

```python
class CreditBudget:
    def __init__(self, client, monthly_budget):
        self.client = client
        self.monthly_budget = monthly_budget
        self.spent_this_month = 0

    async def can_afford(self, credits_needed):
        remaining = self.monthly_budget - self.spent_this_month
        return remaining >= credits_needed

    async def generate_with_budget(self, description):
        if not await self.can_afford(10):
            raise ValueError(f"Budget exceeded: {self.spent_this_month}/{self.monthly_budget}")

        result = await self.client.suno.create_music(
            description=description,
            wait_for_completion=True
        )

        self.spent_this_month += 10
        return result

# Usage
budget = CreditBudget(client, monthly_budget=1000)

try:
    result = await budget.generate_with_budget("rock song")
except ValueError as e:
    print(f"Budget error: {e}")
```

## Purchasing Credits

### Check Pricing

Visit [AI Music API Pricing](https://aimusicapi.ai/pricing) to:

- View subscription plans
- Purchase extra credits
- Upgrade plan
- See pricing tiers

### Programmatic Check

```python
async def check_subscription():
    credits = await client.get_credits()

    print(f"Plan details:")
    print(f"  Total monthly: {credits.total}")
    print(f"  Extra credits: {credits.extra_credits}")
    print(f"  Renewal: {credits.subscription_renewal_date}")

    if credits.available < 100:
        print("\n⚠️ Consider purchasing extra credits or upgrading plan")
```

## Best Practices

### 1. Always Check Credits

```python
# Before batch operations
credits = await client.get_credits()
if credits.available < required_credits:
    print("Not enough credits")
    return
```

### 2. Start Small

```python
# Test with 30s clips first
test_result = await client.suno.create_music(
    description="test",
    duration=30  # Only 10 credits
)

# If good, create full version
if test_result.clips[0].audio_url:
    full_result = await client.suno.create_music(
        description="full version",
        duration=120  # 10 credits
    )
```

### 3. Use Polling vs Webhooks

```python
# Polling - costs credits for status checks (some APIs)
# Webhooks - free, more efficient

# ✅ Preferred: Use webhooks
result = await client.suno.create_music(
    description="...",
    webhook_url="https://mysite.com/webhook",
    wait_for_completion=False
)

# ❌ Less efficient: Frequent polling
while True:
    status = await client.suno.get_music(task_id)
    if status.status == "completed":
        break
    await asyncio.sleep(5)
```

### 4. Cache Results

```python
from functools import lru_cache

@lru_cache(maxsize=100)
async def cached_credits_check():
    """Cache credits for 5 minutes to avoid excessive API calls"""
    return await client.get_credits()
```

### 5. Monitor Usage

```python
# Log all operations
import logging

logger = logging.getLogger(__name__)

async def logged_generate(description):
    credits_before = await client.get_credits()

    result = await client.suno.create_music(
        description=description,
        wait_for_completion=True
    )

    credits_after = await client.get_credits()
    used = credits_before.available - credits_after.available

    logger.info(f"Generated music: used {used} credits, {credits_after.available} remaining")

    return result
```

## Troubleshooting

### Unexpected Credit Usage

```python
# Track operations precisely
async def debug_credits():
    before = await client.get_credits()
    print(f"Before: {before.available}")

    result = await client.suno.create_music(...)

    after = await client.get_credits()
    print(f"After: {after.available}")
    print(f"Used: {before.available - after.available}")
```

### Credits Not Updating

- Check if subscription renewed
- Verify payment method
- Contact support with request ID
- Check dashboard for transactions

### Over-Budget

- Set up alerts at 80% usage
- Monitor daily usage
- Implement rate limiting
- Use webhooks instead of polling

## Next Steps

- [Error Handling](error-handling.md) - Handle insufficient credits
- [Advanced Features](advanced.md) - Optimize usage patterns
- [Configuration](../configuration.md) - Set up monitoring
