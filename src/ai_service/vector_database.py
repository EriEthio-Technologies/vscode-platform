import logging

class VectorDatabase:
    """
    Mock implementation of the VectorDatabase class.
    """
    def __init__(self, embedding_size: int = 768):
        self.embedding_size = embedding_size
        self.data = {}  # Store embeddings and associated code

    def query(self, embedding, project_id: str = "default_project", top_k: int = 5):
        """
        Mock implementation of the query method.
        """
        logging.info(f"Querying vector database for project: {project_id} with embedding: {embedding[:20]}...")
        # In a real implementation, this would perform a similarity search
        # For the mock, return some dummy code if the project exists, else an empty string
        if project_id in self.data:
            return self.data[project_id]
        else:
            return ""

    def add(self, project_id: str, code: str, embedding):
        """
        Mock implementation of adding code and its embedding to the database.
        """
        logging.info(f"Adding code to project: {project_id} with embedding: {embedding[:20]}...")
        self.data[project_id] = code

    def __repr__(self):
        return f"VectorDatabase(embedding_size={self.embedding_size}, data_size={len(self.data)})"
