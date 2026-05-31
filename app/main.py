from fastapi import FastAPI, Query
from app.data_gen import generate_documents
from app.engine import VectorSearchEngine

# 1. Initialize the FastAPI Application
app = FastAPI(title="MVP Semantic Search Engine")

# 2. Instantiate our Naive Vector Search Engine
# This loads the SentenceTransformer model when the file is imported/started
engine = VectorSearchEngine()

# We keep a global reference of current documents in memory
current_docs = []

@app.on_event("startup")
def startup_event():
    """
    Startup hook: Automatically generates 1,000 mock documents and builds
    the initial index, so the API is immediately ready for search.
    """
    global current_docs
    print("Startup: Automatically building initial index for 1,000 documents...")
    
    # Generate 1,000 high-quality mock documents
    current_docs = generate_documents(1000)
    
    # Build the FAISS flat index
    engine.build_index(current_docs)
    print("Startup: Initial index built successfully!")

@app.get("/api/search")
def search(q: str = Query(..., description="The semantic search query"), limit: int = 10):
    """
    Exposes semantic search via a simple GET endpoint.
    Example: GET /api/search?q=vector databases&limit=5
    """
    # Simply call the engine's search function and return the results
    search_results = engine.search(query=q, limit=limit)
    return search_results

@app.get("/api/status")
def status():
    """
    Returns the basic health/status of our search engine.
    """
    return {
        "status": "ready",
        "document_count": len(current_docs),
        "index_type": "FlatL2"
    }

@app.post("/api/index/rebuild")
def rebuild_index(dataset_size: int = Query(1000, description="Number of documents to generate")):
    """
    Triggers a rebuild of the index with a fresh set of N documents.
    """
    global current_docs
    
    # Generate a fresh set of documents
    current_docs = generate_documents(dataset_size)
    
    # Rebuild the index (synchronously for now)
    stats = engine.build_index(current_docs)
    
    return {
        "message": "Index rebuilt successfully",
        "stats": stats
    }
