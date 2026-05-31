import time
from app.data_gen import generate_documents

def test_generate_documents_schema():
    """
    Validates that the generated documents match the required schema.
    """
    count = 100
    docs = generate_documents(count)
    
    assert len(docs) == count
    
    # Check the first document schema
    first_doc = docs[0]
    required_keys = {"id", "title", "body", "category", "timestamp", "word_count"}
    
    for key in required_keys:
        assert key in first_doc, f"Missing key: {key}"
        
    assert first_doc["id"] == "doc_1"
    assert first_doc["category"] == "Technology"  # First is technology based on modulo index
    assert isinstance(first_doc["title"], str)
    assert isinstance(first_doc["body"], str)
    assert isinstance(first_doc["timestamp"], float)
    assert isinstance(first_doc["word_count"], int)
    assert first_doc["word_count"] > 0

def test_generate_documents_diversity():
    """
    Validates that documents have diverse categories and are unique.
    """
    count = 1000
    docs = generate_documents(count)
    
    categories = {doc["category"] for doc in docs}
    assert len(categories) == 4  # All categories should be represented
    
    ids = {doc["id"] for doc in docs}
    assert len(ids) == count  # All IDs must be unique
    
    # Ensure titles are unique
    titles = {doc["title"] for doc in docs}
    assert len(titles) > count // 2  # High diversity in titles

def test_generate_documents_performance():
    """
    Performance test: 100,000 documents must be generated in under 10 seconds.
    Usually takes < 1 second.
    """
    count = 100000
    
    start_time = time.time()
    docs = generate_documents(count)
    end_time = time.time()
    
    elapsed_time = end_time - start_time
    
    print(f"\nGenerated {count} documents in {elapsed_time:.4f} seconds.")
    
    assert len(docs) == count
    assert elapsed_time < 10.0, f"Performance too slow! Took {elapsed_time:.2f} seconds."
