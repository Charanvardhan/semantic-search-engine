## Parent PRD

`issues/prd.md`

## What to build

Set up the project's folder structure, environment configuration, dependencies, and a robust document generation module (`app/data_gen.py`) that can synthetically generate highly realistic and diverse documents (including title, body, category, and metadata) up to 100,000+ scales.

The dependencies will include:
- `fastapi` & `uvicorn` (Async web framework)
- `faiss-cpu` (Vector search library)
- `sentence-transformers` (State-of-the-art embedding model `all-MiniLM-L6-v2`)
- `sqlite3` (Built-in, used for persistent embedding caching)
- `pandas` & `numpy` (Data manipulation)
- `tqdm` (Progress monitoring)
- `requests` & `pytest` (Testing)

The data generator should allow:
- Generating `N` random documents with natural-sounding text (e.g., medical, tech, general topics).
- Generating unique document IDs, clean timestamps, and dynamic tags/metadata.
- High-performance chunk-based writes/caching for dry runs.

## Acceptance criteria

- [ ] `requirements.txt` contains all required packages.
- [ ] `app/data_gen.py` exposes a function `generate_documents(count: int) -> list[dict]` that is extremely fast.
- [ ] A verification script or unit test confirms that 100,000 documents can be generated in under 10 seconds.
- [ ] Generated documents have realistic structure: `id`, `title`, `body`, `category`, `timestamp`, and `word_count`.

## Blocked by

None - can start immediately

## User stories addressed

- User story 1
