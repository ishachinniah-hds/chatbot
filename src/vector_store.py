# src/vector_store.py

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

def create_vector_store(chunks, model_name):
    """
    Sets up ChromaDB vector store given the document chunks. 
    """
    embeddings = HuggingFaceBgeEmbeddings(model_name=model_name)
    doc_search = Chroma.from_documents(chunks, embeddings)
    retriever = doc_search.as_retriever(
        search_type="mmr",
        search_kwargs={'k': 5, 'lambda_mult': 0.25}
    )
    return retriever