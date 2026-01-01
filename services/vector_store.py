from langchain_community.vectorstores import FAISS
from services.embeddings import get_embedding_model


def create_vector_store(chunks):
    """
    Create a FAISS vector store from text chunks
    """
    embeddings = get_embedding_model()
    vector_store = FAISS.from_texts(chunks, embeddings)
    return vector_store

