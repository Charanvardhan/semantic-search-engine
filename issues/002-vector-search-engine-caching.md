## Parent PRD

`issues/prd.md`

## What to build

Implement the core search indexer and similarity search engine in `app/engine.py`. This component handles:
1. **Embedding Generation**: Using `sentence-transformers/all-MiniLM-L6-v2` to map document text to 384-dimensional dense vectors.
2. **Embedding Cache**: A persistent SQLite store (`data/embeddings_cache.db`) mapping the SHA-256 hash of a document's body/title to its generated float array embedding.
3. **FAISS IVFFlat Indexing**: 
   - Dynamically configures FAISS based on the document scale.
   - For smaller datasets ($N < 1000$), uses exhaustive `IndexFlatL2` or `IndexFlatIP`.
   - For larger datasets ($N \ge 1000$), trains an `IndexIVFFlat` coarse quantizer.
   - Saves/loads the trained index from disk (`data/faiss_index.bin`).
4. **Semantic Search**: Computes similarity scores and returns the top-$K$ nearest neighbors, with configurable `nprobe`.

## Acceptance criteria

- [ ] SQLite database `embeddings_cache.db` successfully reads/writes vector embeddings as BLOBs or serialized arrays.
- [ ] Embedding generation utilizes cache: rebuilding the index for 10K identical documents should complete in $< 1$ second (excluding FAISS load time) if cached, validating a $>99\%$ reduction in rebuild time.
- [ ] FAISS IVFFlat indexing trains and populates properly, and returns valid search hits.
- [ ] Semantic query searches can run on both Flat and IVFFlat configurations.
- [ ] Vector normalization is implemented to support cosine similarity if using IP (Inner Product).

## Blocked by

- Blocked by `issues/001-setup-dependencies-data-generation.md`

## User stories addressed

- User story 3
- User story 4
