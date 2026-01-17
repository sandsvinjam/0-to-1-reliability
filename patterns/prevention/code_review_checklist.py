## Reliability Code Review Checklist

### Error Handling
- [ ] All external calls wrapped in try/catch
- [ ] Specific exception types caught (not generic Exception)
- [ ] Errors logged with context
- [ ] User-friendly error messages returned

### Timeouts & Retries
- [ ] All network calls have explicit timeouts
- [ ] Timeout values justified and documented
- [ ] Retry logic uses exponential backoff
- [ ] Maximum retry attempts defined
- [ ] Idempotency considered for retry scenarios

### Resource Management
- [ ] Database connections properly closed
- [ ] File handles released in finally blocks
- [ ] Memory-intensive operations bounded
- [ ] Background threads properly terminated

### Observability
- [ ] Metrics instrumented (success rate, latency)
- [ ] Relevant logs at appropriate levels
- [ ] Distributed tracing context propagated
- [ ] Alert thresholds defined for new endpoints

### Graceful Degradation
- [ ] Fallback behavior defined for dependency failures
- [ ] Circuit breakers implemented for external services
- [ ] Feature flags added for new risky features
- [ ] Degradation modes documented
