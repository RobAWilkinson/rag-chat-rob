from qdrant_client import QdrantClient
from llama_index.vector_stores.qdrant import QdrantVectorStore
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core.ingestion import IngestionPipeline, IngestionCache
import os

# Set up the embedding model globally
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
Settings.embed_model = embed_model

collection_name = "chat_with_notes"
client = QdrantClient(
    url="http://localhost",
    port=6333
)

vector_store = QdrantVectorStore(
    client=client,
    collection_name=collection_name,
)

# Create cache directory if it doesn't exist
cache_dir = "./cache"
os.makedirs(cache_dir, exist_ok=True)

# Initialize the ingestion cache
ingestion_cache = IngestionCache(
    cache_dir=cache_dir,
)

loader = SimpleDirectoryReader(
    input_dir="/Users/rob/Documents/obsidian-notes",
    required_exts=[".txt", ".md"],
    recursive=True
)
documents = loader.load_data()
pipeline = IngestionPipeline(
    transformations=[
        embed_model
    ],
    vector_store=vector_store,
    cache=ingestion_cache  # Add the cache to the pipeline
)

# run the pipeline
nodes = pipeline.run(
    documents=documents,
    show_progress=True  # Optional: shows progress bar
)

index = VectorStoreIndex.from_vector_store(vector_store)
