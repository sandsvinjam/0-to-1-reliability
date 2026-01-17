# Circuit breakers for all external dependencies
from circuitbreaker import circuit

@circuit(failure_threshold=5, recovery_timeout=60)
def call_payment_gateway(payment_data):
    return payment_gateway.process(payment_data)

# Bulkheads to isolate failures
from concurrent.futures import ThreadPoolExecutor

payment_executor = ThreadPoolExecutor(max_workers=10)  # Isolated thread pool
search_executor = ThreadPoolExecutor(max_workers=20)   # Separate pool

# Retries with exponential backoff and jitter
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10) + wait_random(0, 2)
)
def call_with_retry(func, *args):
    return func(*args)
