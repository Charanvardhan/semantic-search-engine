import time
import concurrent.futures
import numpy as np
from app.data_gen import generate_documents

# A collection of diverse test queries covering Technology, Medicine, Finance, and General topics
MOCK_QUERIES = [
    "optimizing vector database indexing performance",
    "fast approximate nearest neighbor similarity searches",
    "async fastapi endpoints under parallel thread execution",
    "CRISPR gene editing clinical trial results",
    "targeted mRNA vaccine cellular delivery pathways",
    "cardiovascular blood flow biological simulations",
    "high-frequency algorithmic portfolio arbitrage risk",
    "macroeconomic inflation rate interest curves analysis",
    "federal reserve market volatility indices prediction",
    "sustainable urban organic gardening cooperative",
    "single-origin coffee bean thermodynamic roasting guide",
    "traditional sourdough bread fermentation techniques"
]

def run_load_test(engine, queries: list[str], concurrent_workers: int = 10) -> dict:
    """
    Simulates a concurrent stream of search requests against the search engine.
    Measures tail latencies (percentiles) and sustained QPS throughput.
    """
    total_queries = len(queries)
    latencies_ms = []
    
    # We use a ThreadPoolExecutor to simulate multiple parallel search clients
    start_total_time = time.perf_counter()
    
    def single_query_worker(query: str) -> float:
        """
        Executes a single search request and records its microsecond-precision latency.
        """
        start_req = time.perf_counter()
        # Trigger the engine's naive search
        engine.search(query, limit=5)
        end_req = time.perf_counter()
        
        # Return duration in milliseconds
        return (end_req - start_req) * 1000

    # Execute all queries concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_workers) as executor:
        # Submit all tasks and gather results as they complete
        futures = [executor.submit(single_query_worker, q) for q in queries]
        for future in concurrent.futures.as_completed(futures):
            try:
                latency = future.result()
                latencies_ms.append(latency)
            except Exception as e:
                print(f"Error executing query: {e}")
                
    end_total_time = time.perf_counter()
    total_elapsed = end_total_time - start_total_time
    
    # Compute performance metrics using numpy percentiles
    latencies_ms = np.array(latencies_ms)
    p50 = float(np.percentile(latencies_ms, 50))
    p90 = float(np.percentile(latencies_ms, 90))
    p95 = float(np.percentile(latencies_ms, 95))
    p99 = float(np.percentile(latencies_ms, 99))
    
    # QPS = total queries completed divided by total time elapsed
    qps = total_queries / total_elapsed if total_elapsed > 0 else 0.0
    
    return {
        "queries_run": total_queries,
        "concurrent_workers": concurrent_workers,
        "total_time_seconds": total_elapsed,
        "qps": qps,
        "latency_stats": {
            "p50_ms": p50,
            "p90_ms": p90,
            "p95_ms": p95,
            "p99_ms": p99
        }
    }

def run_scale_benchmark(engine, scales: list[int] = [1000, 5000, 10000]) -> list[dict]:
    """
    Runs a full automated benchmarking suite across multiple document scales.
    Saves and returns benchmarking stats for plotting or rendering.
    """
    results = []
    print(f"\n=== Starting Automated Benchmarking Suite across scales: {scales} ===")
    
    # We duplicate mock queries to create a robust query batch size (e.g. 50 parallel requests)
    test_queries = MOCK_QUERIES * 4  # 48 total parallel search queries
    
    for scale in scales:
        print(f"\n--- Benchmarking Scale: {scale} Documents ---")
        
        # 1. Generate new documents
        print(f"Generating {scale} documents...")
        docs = generate_documents(scale)
        
        # 2. Measure Index Rebuild Time
        print("Rebuilding index...")
        build_start = time.time()
        build_stats = engine.build_index(docs)
        build_duration = time.time() - build_start
        print(f"Index built in {build_duration:.4f} seconds.")
        
        # 3. Measure Search Throughput and Latencies under concurrent load
        print(f"Running concurrent search load test ({len(test_queries)} queries, 10 workers)...")
        load_stats = run_load_test(engine, test_queries, concurrent_workers=10)
        
        print(f"Results for {scale} docs:")
        print(f"  - Index Rebuild Time: {build_duration:.2f} seconds")
        print(f"  - QPS (Throughput): {load_stats['qps']:.2f} queries/sec")
        print(f"  - p95 Tail Latency: {load_stats['latency_stats']['p95_ms']:.2f} ms")
        
        # Compile complete log metrics
        results.append({
            "document_count": scale,
            "rebuild_time_seconds": build_duration,
            "qps": load_stats["qps"],
            "latencies": load_stats["latency_stats"],
            "index_type": build_stats["index_type"]
        })
        
    print("\n=== Benchmarking Suite Completed! ===")
    return results
