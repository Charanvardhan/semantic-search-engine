import time
import os
import math
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Dimension of all-MiniLM-L6-v2 embeddings
EMBEDDING_DIM = 384

# Minimum number of documents to justify training an IVFFlat index.
# Below this threshold we fall back to exact FlatL2.
IVF_THRESHOLD = 1000


class VectorSearchEngine:
    """
    Upgraded Search Engine using FAISS IVFFlat for Approximate Nearest Neighbor (ANN) search.

    Index selection at build time:
      - N < IVF_THRESHOLD  →  IndexFlatL2  (exact, good for small corpora)
      - N >= IVF_THRESHOLD →  IndexIVFFlat (ANN, sub-linear search for large corpora)

    IVFFlat key parameters:
      nlist  — number of Voronoi cells (partitions). Rule: sqrt(N), clamped to [4, N//4].
               More cells = faster search but lower recall if nprobe is kept fixed.
      nprobe — cells visited per query (set on the index before search).
               Rule: nlist // 10.  Higher nprobe = better recall, higher latency.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        index_path: str = "data/faiss_index.bin",
    ):
        print(f"Initializing Search Engine with model: {model_name}...")
        self.model = SentenceTransformer(model_name)
        self.index_path = index_path
        self.index = None
        self.documents = []

        # Metadata about the currently loaded index
        self._index_type: str = "none"
        self._nlist: int = 0
        self._nprobe: int = 1

        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _compute_nlist(self, n: int) -> int:
        """
        Compute the number of IVF Voronoi cells.

        Rule: sqrt(N), clamped so we always have at least 4 training vectors
        per cell (FAISS hard requirement: n >= nlist).
        """
        raw = int(math.sqrt(n))
        # Never exceed N//4 so every cell gets meaningful training coverage.
        return max(4, min(raw, n // 4))

    # ------------------------------------------------------------------
    # Build
    # ------------------------------------------------------------------

    def build_index(self, documents: list[dict], force_rebuild: bool = False) -> dict:
        """
        Encode all document bodies and build the appropriate FAISS index.

        Steps:
          1. Encode all document bodies into float32 embeddings [N, 384].
          2. Choose index type based on N:
               • N < 1000  → IndexFlatL2  (brute-force, exact)
               • N >= 1000 → IndexIVFFlat (ANN, trained on the full embedding matrix)
          3. Add all embeddings to the index.
          4. Persist the index to disk.
        """
        start_time = time.time()
        self.documents = documents
        n = len(documents)

        print(f"Building index for {n} documents...")

        # Step 1 — Embed all document bodies
        texts = [doc["body"] for doc in documents]
        embeddings = self.model.encode(
            texts, show_progress_bar=False, convert_to_numpy=True
        )
        embeddings = embeddings.astype("float32")

        # L2-normalize vectors to support Cosine Similarity via Inner Product (IP)
        faiss.normalize_L2(embeddings)

        # Step 2+3 — Build the FAISS index
        if n < IVF_THRESHOLD:
            # Small corpus: exact brute-force Cosine Similarity search, no training needed.
            print(f"  → Using IndexFlatIP (N={n} < {IVF_THRESHOLD}, Cosine Similarity search).")
            self.index = faiss.IndexFlatIP(EMBEDDING_DIM)
            self.index.add(embeddings)
            self._index_type = "FlatIP"
            self._nlist = 0
            self._nprobe = 1

        else:
            # Large corpus: train an IVFFlat ANN index.
            nlist = self._compute_nlist(n)
            nprobe = max(1, nlist // 10)
            print(
                f"  → Using IndexIVFFlat (N={n}, nlist={nlist}, nprobe={nprobe}, Cosine Similarity search)."
            )

            # Coarse quantizer: a flat IP index that maps each vector to its nearest centroid.
            quantizer = faiss.IndexFlatIP(EMBEDDING_DIM)

            # IVFFlat partitions the space into nlist Voronoi cells.
            # Training runs k-means on the embeddings to learn the centroids.
            self.index = faiss.IndexIVFFlat(
                quantizer, EMBEDDING_DIM, nlist, faiss.METRIC_INNER_PRODUCT
            )
            print(f"  → Training IVFFlat on {n} vectors...")
            self.index.train(embeddings)   # learns nlist centroids via k-means
            self.index.add(embeddings)     # assigns each vector to its nearest centroid cell
            self.index.nprobe = nprobe     # cells to scan per query (recall vs latency knob)

            self._index_type = f"IVFFlat(nlist={nlist}, FlatIP)"
            self._nlist = nlist
            self._nprobe = nprobe

        # Step 4 — Persist to disk
        faiss.write_index(self.index, self.index_path)

        duration = time.time() - start_time
        print(f"Index build completed in {duration:.4f}s  [{self._index_type}]")

        return {
            "duration_seconds": duration,
            "document_count": n,
            "index_type": self._index_type,
            "nlist": self._nlist,
            "nprobe": self._nprobe,
        }

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    def search(self, query: str, limit: int = 10, nprobe: int = None) -> dict:
        """
        Embed the query and run ANN (or exact) search against the loaded index.

        Args:
            query:  The user's natural-language search string.
            limit:  Maximum number of results to return.
            nprobe: Override the default nprobe for this query only.
                    Higher → better recall, higher latency.
                    Only applies when the index is IVFFlat.
        """
        if self.index is None or not self.documents:
            raise ValueError("Index is not loaded or built yet. Call build_index() first.")

        start_time = time.time()

        # Apply per-query nprobe override (IVFFlat only)
        if nprobe is not None and hasattr(self.index, "nprobe"):
            self.index.nprobe = nprobe

        # Encode the query into a single float32 vector
        query_vector = (
            self.model.encode([query], convert_to_numpy=True).astype("float32")
        )

        # Normalize the query vector to unit length (critical for Cosine Similarity)
        faiss.normalize_L2(query_vector)

        # Run ANN (or exact) search — returns top-limit (distance, index) pairs
        distances, indices = self.index.search(query_vector, limit)

        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                # FAISS returns -1 when fewer than `limit` results exist
                continue
            doc = self.documents[idx]
            results.append(
                {
                    "id": doc["id"],
                    "score": float(dist),  # Cosine Similarity score (higher = more similar)
                    "title": doc["title"],
                    "body": doc["body"],
                    "category": doc["category"],
                    "metadata": {"word_count": doc["word_count"]},
                }
            )

        latency_ms = (time.time() - start_time) * 1000

        return {
            "query": query,
            "latency_ms": latency_ms,
            "index_type": self._index_type,
            "results": results,
        }
