import time
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorSearchEngine:
    """
    Minimum Viable Product (MVP) Search Engine.
    - No Caching.
    - Direct exact L2 search (IndexFlatL2).
    - Extremely simple and easy to understand!
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", index_path: str = "data/faiss_index.bin"):
        print(f"Initializing Naive Search Engine with model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.index_path = index_path
        self.index = None
        self.documents = []  # Keep original documents in memory
        
        # Ensure directories exist
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)

    def build_index(self, documents: list[dict], force_rebuild: bool = False) -> dict:
        """
        Naive indexing: 
        1. Compiles list of document bodies.
        2. Encodes all bodies to vectors using SentenceTransformers.
        3. Stores them in a flat brute-force FAISS index.
        """
        start_time = time.time()
        self.documents = documents
        n = len(documents)
        
        print(f"MVP: Building index for {n} documents...")
        
        # Extract text bodies to be encoded
        texts = [doc["body"] for doc in documents]
        
        # Encode all texts into a 2D numpy array [N, 384]
        embeddings = self.model.encode(texts, show_progress_bar=False, convert_to_numpy=True)
        embeddings = embeddings.astype("float32")
        
        # Setup exact L2 Euclidean distance index (384 dimensions)
        self.index = faiss.IndexFlatL2(384)
        self.index.add(embeddings)
        
        # Save index to disk
        faiss.write_index(self.index, self.index_path)
        
        duration = time.time() - start_time
        print(f"MVP: Index build completed in {duration:.4f} seconds.")
        
        return {
            "duration_seconds": duration,
            "document_count": n,
            "index_type": "FlatL2",
            "cache_hit_rate": 0.0,
            "cache_hits": 0,
            "cache_misses": n
        }

    def search(self, query: str, limit: int = 10) -> dict:
        """
        MVP search:
        1. Embed the search query on the fly.
        2. Perform exact flat brute-force scan.
        """
        if self.index is None or not self.documents:
            raise ValueError("Index is not loaded or built yet.")
            
        start_time = time.time()
        
        # Embed user's query
        query_vector = self.model.encode([query], convert_to_numpy=True).astype("float32")
        
        # Perform brute-force exact L2 search
        distances, indices = self.index.search(query_vector, limit)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            doc = self.documents[idx]
            results.append({
                "id": doc["id"],
                "score": float(dist),  # L2 distance
                "title": doc["title"],
                "body": doc["body"],
                "category": doc["category"],
                "metadata": {"word_count": doc["word_count"]}
            })
            
        latency_ms = (time.time() - start_time) * 1000
        
        return {
            "query": query,
            "latency_ms": latency_ms,
            "results": results
        }
