## Parent PRD

`issues/prd.md`

## What to build

Create a stunning, premium, state-of-the-art Single Page Application (SPA) dashboard in `app/static/index.html` (with styling/js files or self-contained) served from the FastAPI `/` route.

Design Guidelines:
- **Rich Aesthetics**: Glowing neon-violet/emerald dark mode, glassmorphism, responsive grid layout, clean modern typography (e.g., Google Fonts 'Outfit' and 'Plus Jakarta Sans'), custom SVGs, and smooth micro-interactions.
- **Search Playground**:
  - A real-time semantic search input bar with autocomplete/sample suggestions.
  - Interactive search result cards showing document title, text, category badges, metadata, and the FAISS distance/similarity score.
  - Precision latency tag (e.g. "Completed in 4.12 ms").
- **Analytics & Benchmarking**:
  - Rich interactive charts (using Chart.js or similar) plotting p95 latency and QPS across scales (10K, 25K, 50K, 100K).
  - Stat cards for: Total Indexed Docs, Model Dimension, Rebuild Time (With Cache vs Without), Cache Hit Rate, and current QPS.
- **Index Management**:
  - Form to trigger async index rebuilds for different scales (10K to 100K documents).
  - Live progress bar/spinning indicator pulling status from the `/api/status` endpoint.

## Acceptance criteria

- [ ] The dashboard loads perfectly on the `/` root route.
- [ ] Interface is highly responsive, gorgeous, and fully matches premium styling requirements (no generic colors or basic text layouts).
- [ ] Users can type queries in the search playground, hit enter or search, and instantly see dynamic results with exact scores and latency tags.
- [ ] Benchmark statistics and line/bar charts render beautifully, fetching live data from `/api/benchmark/results`.
- [ ] Triggering an index rebuild shows a visual progress indicator and live updates without blocking the browser.

## Blocked by

- Blocked by `issues/004-benchmarking-runner.md`

## User stories addressed

- User story 6
