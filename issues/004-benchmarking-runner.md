## Parent PRD

`issues/prd.md`

## What to build

Implement a high-speed parallel query benchmarking suite in `app/benchmark.py` and expose it via the API. This module evaluates the system's search latency (p50, p90, p95, p99) and Queries Per Second (QPS) across diverse document scales: 10,000, 25,000, 50,000, and 100,000 documents.

Features:
1. **Benchmark Engine**: Simulates concurrent query requests (using standard query pools) to measure how the FAISS index scales.
2. **Dynamic Metrics Collection**:
   - Calculates p50, p90, p95, and p99 latency in milliseconds.
   - Computes sustained QPS under concurrent load.
   - Summarizes embedding reuse impact (index rebuild time vs cache hit rate).
3. **API Endpoints**:
   - **POST `/api/benchmark/run`**: Triggers a full benchmark run across standard sizes. Runs as a background task.
   - **GET `/api/benchmark/results`**: Retrieves historical benchmark logs and current data points for graphing.

## Acceptance criteria

- [ ] Benchmarking module handles concurrent search query testing safely without memory leaks.
- [ ] Latency percentiles (p50, p90, p95, p99) and QPS are calculated accurately using high-precision timers.
- [ ] Benchmarking runs at the 100,000 document scale and validates that p95 search latency is successfully under 100ms.
- [ ] API endpoints return structured JSON ready for graphing in the frontend.

## Blocked by

- Blocked by `issues/003-async-fastapi-backend.md`

## User stories addressed

- User story 5
