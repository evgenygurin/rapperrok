# Exceptions Reference

Complete exception hierarchy and error handling.

For detailed usage examples and guides, see the [Error Handling Guide](../guides/error-handling.md).

## Exception Hierarchy

- `AIMusicAPIError` - Base exception
  - `AuthenticationError` - Authentication failures
  - `RateLimitError` - Rate limiting
  - `InsufficientCreditsError` - Not enough credits
  - `InvalidParameterError` - Invalid parameters
  - `TaskFailedError` - Generation failed
  - `NetworkError` - Network issues
  - `TimeoutError` - Request timeout

See the [Error Handling Guide](../guides/error-handling.md) for complete documentation and examples.
