# Product Requirements Document (PRD)

## Problem Statement

As dataset sizes scale to hundreds of thousands of documents, building a high-performance semantic search engine requires managing two critical bottlenecks:
1. **Embedding Generation Time**: Generating high-dimensional vector embeddings for 100,000+ documents is computationally expensive, especially on CPUs. Re-calculating embeddings from scratch for unchanged documents during index rebuilds is highly inefficient.
2. **Search Latency**: Executing exhaustive brute-force exact vector searches across high-dimensional space for large datasets causes unacceptable response times (often hundreds of milliseconds). We need sub-100ms p95 latencies and high Query Per Second (QPS) throughput.

## Solution

A Semantic Search Engine utilizing **FAISS IVFFlat (Inverted File Flat)** for Approximate Nearest Neighbor (ANN) search, an **Embedding Reuse Cache** to bypass model inference for unchanged documents during index updates, and a highly responsive, async **FastAPI** query layer. 

The system features:
- **FastAPI Async Backend**: Handles search requests, asynchronous index updates, and benchmarking triggers without blocking search clients.
- **FAISS IVFFlat Indexing**: Accelerates vector similarity search by clustering the vector space and scanning only a fraction of the documents.
- **Embedding Reuse Cache**: Persists document hashes and their corresponding high-dimensional embeddings using a highly efficient storage layer (SQLite or local binary storage) to reduce indexing times from hours to seconds for incremental updates.
- **Dynamic Benchmarking Dashboard**: A gorgeous, state-of-the-art dark-mode glassmorphic dashboard showcasing live semantic searches, real-time search latencies, index rebuild configurations, and interactive performance charts (QPS and p95 latency benchmarks across 10K, 25K, 50K, and 100K scales).

## User Stories

1. As a system administrator, I want to upload or generate datasets of up to 100,000 documents, so that I can evaluate the system's performance at large scale.
2. As a system administrator, I want to trigger an asynchronous index rebuild using an IVFFlat index, so that I can keep the search database updated without blocking incoming searches.
3. As a developer, I want to reuse previously generated embeddings when rebuilding the index, so that incremental document additions or updates complete in seconds rather than hours.
4. As a product developer, I want to search through 100,000+ documents semantically and receive relevant results in under 100ms p95 latency.
5. As a QA / Performance engineer, I want to run a suite of automated latency and QPS benchmarks across 10K, 25K, 50K, and 100K document scales, so that I can validate that p95 search latency remains sub-100ms.
6. As a business stakeholder, I want a beautiful, premium analytics dashboard to visualize the search playground, search speeds (with microsecond precision), and dynamic benchmarking charts.

## Implementation Decisions

### 1. Key Modules & Sub-systems
- **Data Generator (`app/data_gen.py`)**: Responsible for synthesising high-quality mock document collections (including titles, bodies, categories, and custom metadata) up to 100,000+ items.
- **Vector Search Engine (`app/engine.py`)**: 
  - **SentenceTransformers**: Use `all-MiniLM-L6-v2` (384-dimensional dense vectors) for fast and accurate embedding generation on CPU/GPU.
  - **FAISS IVFFlat**: Cluster embeddings using an inverted file structure (`IndexIVFFlat`). Train the index on a subset of vectors, then add all vectors.
  - **Embedding Cache**: A SQLite database storing `sha256(text) -> list[float]` embeddings to bypass model inference for previously processed documents.
- **Benchmark Suite (`app/benchmark.py`)**: Measures search latency (p50, p90, p95, p99) and QPS under parallel execution across multiple dataset scales.
- **Web API Layer (`app/main.py`)**: Asynchronous FastAPI endpoints, including `/search`, `/index`, `/status`, `/benchmark/run`, and `/benchmark/results`.
- **Aesthetic Frontend (`app/static/index.html`)**: Single-page modern dashboard with a neon dark-mode style, custom glassmorphism, search analytics, and interactive benchmarking charts.

### 2. FAISS Index Configuration
- Metric: L2 Euclidean distance or Inner Product (Cosine Similarity after normalization).
- Quantizer: `IndexFlatL2` as the coarse quantizer.
- Number of Voronoi cells (`nlist`): Scaled dynamically (e.g., $4 \times \sqrt{N}$ where $N$ is the dataset size).
- Search probes (`nprobe`): Configurable at search time to trade off recall and latency.

### 3. API Contract Examples

#### **GET `/api/search`**
- Query Parameters: `q` (string), `limit` (int), `nprobe` (int)
- Response:
```json
{
  "query": "vector databases",
  "latency_ms": 12.45,
  "results": [
    {
      "id": "doc_12345",
      "score": 0.895,
      "title": "Introduction to FAISS",
      "body": "FAISS is a library for efficient similarity search...",
      "metadata": {"category": "Tech", "words": 150}
    }
  ]
}
```

#### **POST `/api/index/rebuild`**
- Body Parameters: `dataset_size` (int), `force_rebuild` (bool)
- Response:
```json
{
  "task_id": "index_task_abc",
  "status": "queued",
  "message": "Asynchronous index rebuild started."
}
```

#### **GET `/api/status`**
- Response:
```json
{
  "status": "ready",
  "indexing_in_progress": false,
  "index_stats": {
    "document_count": 100000,
    "vector_dimensions": 384,
    "index_type": "IVF1024,Flat",
    "trained": true,
    "cache_hit_rate": 0.985,
    "memory_bytes": 153600000
  }
}
```

## Testing Decisions

- **Performance Tests**: Direct python scripts (`app/benchmark.py`) simulating concurrent requests, measuring execution latency with standard time models.
- **Verification Tests**: Unit tests confirming that:
  - Vector similarity search returns expected results (semantic sanity check).
  - FAISS index is properly trained and returns values within `<100ms`.
  - Embedding cache hit reduces build time by $>90\%$ (i.e. model execution is bypassed).
  
## Out of Scope
- Distributed clustering of FAISS across multiple nodes.
- GPU acceleration optimization (focus is CPU-bound sub-100ms scaling).
- Production-grade authentication or user tenancy.

## Further Notes
- Dynamic charts on the dashboard will use Chart.js via CDN for responsive, visually striking animations.
- The UI features a glassmorphic design utilizing a tailwind-inspired premium theme with customized glowing borders and micro-interactions.
