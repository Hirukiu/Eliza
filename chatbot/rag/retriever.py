import os
import sys
import numpy as np

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from ingest import EmbeddingManager, ChromaDBManager

embedding_manager = EmbeddingManager()
db_manager = ChromaDBManager()

def query(question: str, n_results: int = 3):
    embedding = embedding_manager.generate_embeddings([question])
    results = db_manager.collection.query(
        query_embeddings=embedding.tolist(),
        n_results=n_results
    )
    return results["documents"][0]

if __name__ == "__main__":
    question = "Comment poser des congés ?"
    chunks = query(question)
    for i, chunk in enumerate(chunks):
        print(f"\n Results {i+1} \n{chunk}")