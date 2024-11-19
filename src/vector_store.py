# src/vector_store.py

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

def create_vector_store(chunks, model_name="sentence-transformers/all-mpnet-base-v2"):
    """
    Set up ChromaDB vector store given the document chunks. 

    Args:
        chunks (list): List of document chunks to index
        model_name (str): The name of the Hugging Face embeddign model to use. 

    Returns:
        retriever object to retrieve similar documents based on the query. 
    """
    embeddings = HuggingFaceBgeEmbeddings(model_name=model_name)
    doc_search = Chroma.from_documents(chunks, embeddings)
    retriever = doc_search.as_retriever(
        search_type="mmr",
        search_kwargs={'k': 5, 'lambda_mult': 0.25}
    )
    return retriever