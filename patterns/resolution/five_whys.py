Why 1: Why did payments fail?
Answer: Payment gateway returned timeouts

Why 2: Why did the gateway timeout?
Answer: Our requests took too long (>5 seconds)

Why 3: Why were our requests slow?
Answer: Database queries in payment flow increased from 3 to 12

Why 4: Why did we add 9 extra queries?
Answer: New feature fetched user's full transaction history

Why 5: Why did we fetch full history?
Answer: Developer didn't realize it would be queried on every payment

ROOT CAUSE: Lack of performance testing before deployment
