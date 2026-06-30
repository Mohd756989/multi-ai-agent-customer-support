from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import os


class LongTermMemory:
    def __init__(self):
        self.path = "memory_store"

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )

        if os.path.exists(self.path):
            self.vector_store = FAISS.load_local(
                self.path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        else:
            self.vector_store = FAISS.from_texts(
                ["Initial memory"],
                self.embeddings
            )

    def save_memory(self, user_id, text):
        self.vector_store.add_texts(
            [text],
            metadatas=[{"user_id": user_id}]
        )
        self.vector_store.save_local(self.path)

    def retrieve_memory(self, query, user_id):
        docs = self.vector_store.similarity_search(
            query,
            k=3
        )

        return [
            doc.page_content
            for doc in docs
            if doc.metadata.get("user_id") == user_id
        ]