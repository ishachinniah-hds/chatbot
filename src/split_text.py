# src/split.py

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import Language

def split_documents(documents, chunk_size, chunk_overlap):
    """
    Splits the document into smaller chunks recursively
    """
    text_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.PYTHON, chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    return text_splitter.split_documents(documents)