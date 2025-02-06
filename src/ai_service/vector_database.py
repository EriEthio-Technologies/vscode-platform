import logging
import chromadb
from chromadb.utils import embedding_functions

class VectorDatabase:
    """
    Vector database implementation using ChromaDB.
    """
    def __init__(self, client_settings=chromadb.Settings(anonymized_telemetry=False)):
        self.client = chromadb.PersistentClient(path="vsCode_assistant", settings=client_settings)
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            api_key=None, # can be set to None when used locally
            model_name="all-mpnet-base-v2"
        )
        self.collection = self.client.get_or_create_collection(
            name="vsCode_assistant_collection",
            embedding_function=self.embedding_function,
            metadata={"hnsw:space": "cosine"} # l2 is the default
        )
        logging.info("VectorDatabase initialized")

    def add(self, embedding, project_id, metadata=None):
        """
        Adds an embedding to the vector database.
        """
        if metadata is None:
            metadata = {}
        metadata["project_id"] = project_id
        self.collection.add(
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[str(len(self.collection.get()['ids']))] # Simple incremental ID
        )
        logging.info(f"Added embedding to vector database for project: {project_id}")

    def query(self, embedding, project_id, n_results=5):
        """
        Queries the vector database for the most similar embeddings.
        """
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=n_results,
            where={"project_id": project_id}
        )
        logging.info(f"Queried vector database for project: {project_id}")
        return results

    def __repr__(self):
        return f"VectorDatabase(client={self.client}, collection={self.collection})"
