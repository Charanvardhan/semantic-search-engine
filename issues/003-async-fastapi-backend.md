## Parent PRD

`issues/prd.md`

## What to build

Implement the scalable asynchronous FastAPI backend in `app/main.py` which provides endpoints for searching, querying status, and triggering index rebuilds.

Endpoints:
1. **GET `/api/search`**:
   - Accepts search query string `q`, `limit` (default: 10), `nprobe` (default: 16).
   - Computes query embedding asynchronously or synchronously, executes FAISS search, and returns matched documents with similarity scores and processing latency in milliseconds.
2. **POST `/api/index/rebuild`**:
   - Triggers an asynchronous index rebuild for a target dataset size (e.g., 10,000 to 100,000 documents) using `BackgroundTasks`.
   - Thread-safe swap: When the new index is fully rebuilt and loaded, it atomically replaces the active FAISS index, ensuring zero downtime for `/api/search` requests.
3. **GET `/api/status`**:
   - Returns metadata about the current index state (number of docs, vector dimensions, trained status, index build date, cache hit statistics, whether rebuild is currently running, rebuild progress percentage).

## Acceptance criteria

- [ ] FastAPI backend starts up and binds successfully.
- [ ] `/api/search` responds under 100ms for active query.
- [ ] `/api/index/rebuild` runs asynchronously in the background. Searching is still functional while the background indexing is running.
- [ ] Index swap is atomic; once rebuild completes, status immediately reflects new document counts and type.
- [ ] Unit tests cover search, status, and rebuild trigger endpoints.

## Blocked by

- Blocked by `issues/002-vector-search-engine-caching.md`

## User stories addressed

- User story 2
- User story 4
- User story 6
