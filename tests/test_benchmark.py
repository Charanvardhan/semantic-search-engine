import pytest
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    """
    Fixture yielding a TestClient instance wrapped in a context manager
    to correctly trigger FastAPI's on_event("startup") events.
    """
    with TestClient(app) as test_client:
        yield test_client

def test_benchmark_api_endpoints(client):
    """
    Integration test: Verifies that the /api/benchmark/run endpoint executes
    performance benchmarks across document scales, and that /api/benchmark/results
    correctly exposes the accumulated metrics.
    """
    # 1. Trigger benchmark run for scale 500 and 1000
    print("\nTriggering benchmark run...")
    response = client.post("/api/benchmark/run?sizes=500,1000")
    assert response.status_code == 200
    data = response.json()
    
    assert data["message"] == "Benchmark completed successfully"
    results = data["results"]
    assert len(results) == 2
    
    # Check the schema of the first benchmark scale results
    first_scale_results = results[0]
    assert first_scale_results["document_count"] == 500
    assert "rebuild_time_seconds" in first_scale_results
    assert "qps" in first_scale_results
    assert "latencies" in first_scale_results
    assert "index_type" in first_scale_results
    
    # Check latency structure
    latencies = first_scale_results["latencies"]
    assert "p50_ms" in latencies
    assert "p95_ms" in latencies
    
    # 2. Retrieve history results and check that they are accumulated
    print("Fetching benchmark history...")
    history_response = client.get("/api/benchmark/results")
    assert history_response.status_code == 200
    history_data = history_response.json()
    
    assert history_data["history_count"] >= 2
    assert len(history_data["results"]) >= 2
    assert history_data["results"][0]["document_count"] == 500
    assert history_data["results"][1]["document_count"] == 1000
