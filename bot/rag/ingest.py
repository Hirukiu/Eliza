import json
import os
import chromadb
import uuid
import numpy as np 
from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer
from chromadb.config import Settings
from typing import List,Dict,Any,Tuple
from sklearn.metrics.pairwise import cosine_similarity 

 

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAQ_PATH = os.path.join(BASE_DIR, "data", "faq.json")

with open(FAQ_PATH, "r", encoding="utf-8") as f:
    faq = json.load(f)

docs = [
    Document(page_content=f"Q: {item['question']}\nR: {item['answer']}")
    for item in faq
]
## Embeddings for DB 

class EmbeddingManager:
    "Handles embedding using SentenceTransformers"
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self._load_model()
        
    def _load_model(self):
        try:
            self.model = SentenceTransformer(self.model_name)
        except Exception as e :
            print(f"Error load : {e}")  
            raise  
    
    def generate_embeddings(self, texts: List[str])-> np.ndarray : 
        if not self.model: 
            raise ValueError('not found')
        embeddings= self.model.encode(texts, show_progress_bar=True)
        return embeddings

##Embedding Manager 
embedding_manager =  EmbeddingManager()

## CHROMADB 
class ChromaDBManager:
    "Handles storage and retrieval in ChromaDB"
    def __init__(self, collection_name: str = "faq_documents", persist_directory: str = os.path.join(BASE_DIR, "..", "data", "vector_store")):
        self.collection_name = collection_name
        self.persist_directory = persist_directory
        self.client = None
        self.collection = None
        self._initialize_store()

    def _initialize_store(self):
        try:
            self.client= chromadb.PersistentClient(path=self.persist_directory)
            self.collection = self.client.get_or_create_collection(
                name = self.collection_name
            )
        except Exception as e :
            print(f"error initilize store : {e}")
            raise
        


    def store_documents(self, docs: List[Document], embeddings: np.ndarray):
        if len(docs) != len(embeddings):
            raise ValueError("match docs embeddings")
    
        ids = [str(uuid.uuid4()) for _ in docs]
        texts = [doc.page_content for doc in docs]
        embeddings_list = embeddings.tolist()
    
        self.collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings_list
        )
        print("documents stored")

    def query(self, query_embedding: np.ndarray, n_results: int = 3):
        results = self.collection.query(
        query_embeddings=query_embedding.tolist(),
        n_results=n_results
        )
    
if __name__ == "__main__":
    texts = [doc.page_content for doc in docs]
    embeddings = embedding_manager.generate_embeddings(texts)
    
    db_manager = ChromaDBManager()
    db_manager.store_documents(docs, embeddings)
    
    print("Ingested success")