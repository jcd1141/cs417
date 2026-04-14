1. When the client times out it means the client stopped waiting for a response. It doesn't mean it failed. The server is usually still doing the request in the background, which is why retries can cause duplicate work.

2. If the idempotency key was random each time, it would not prevent duplicates. The server would think every retry is a new request. It only works when the key stays the same for the same task.

3. It depends on how long the task takes. If it’s fast, use sync so the client gets the result right away. If it's slow we use async so the client doesn’t have to wait and can check back later.

4. The server was keeping track of things like past requests and job progress, but the client couldn’t see it at first. Adding things like the log, job IDs, and status endpoints made that hidden information accessible.