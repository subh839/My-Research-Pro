"""Test configuration and utilities"""

TEST_CONFIG = {
    "chromadb": {
        "test_db_path": "./test_chroma_db",
        "in_memory": True
    },
    "ai_client": {
        "timeout": 30,
        "max_retries": 3
    },
    "search_client": {
        "mock_mode": True,  # Always use mock for tests
        "timeout": 10
    },
    "performance": {
        "max_response_time": 10.0,  # seconds
        "concurrent_users": 5
    }
}

SAMPLE_DOCUMENTS = [
    "Artificial intelligence is transforming modern technology.",
    "Machine learning algorithms require large datasets for training.",
    "Natural language processing enables computers to understand human language.",
    "Computer vision allows machines to interpret visual information.",
    "Deep learning uses neural networks with multiple layers."
]

SAMPLE_METADATA = [
    {"source": "test", "type": "ai", "topic": "introduction"},
    {"source": "test", "type": "ml", "topic": "algorithms"},
    {"source": "test", "type": "nlp", "topic": "fundamentals"},
    {"source": "test", "type": "cv", "topic": "basics"},
    {"source": "test", "type": "dl", "topic": "networks"}
]