# ai-service/context/vector_db.py
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings

class CodeContextManager:
    def __init__(self):
        self.vector_db = Chroma(
            embedding_function=HuggingFaceEmbeddings(),
            persist_directory="./chroma_db"
        )

    def retrieve_context(self, prompt: str, k: int = 3) -> list:
        """Retrieve top-k relevant code snippets."""
        return self.vector_db.similarity_search(prompt, k=k)
