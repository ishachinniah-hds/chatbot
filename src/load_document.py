# document_processor.py

import logging
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_community.document_loaders.parsers.pdf import (
   extract_from_images_with_rapidocr,
)
from langchain.schema import Document

def load_pdf(source):
    loader = PyPDFLoader(source)
    documents = loader.load()

    # Filter out scanned pages
    unscanned_documents = [doc for doc in documents if doc.page_content.strip() != ""]

    scanned_pages = len(documents) - len(unscanned_documents)
    if scanned_pages > 0:
        logging.info(f"Omitted {scanned_pages} scanned page(s) from the PDF.")

    if not unscanned_documents:
        raise ValueError(
            "All pages in the PDF appear to be scanned. Please use a PDF with text content."
       )
    
    return unscanned_documents

def load_image(source):
   # Extract text from image using OCR
    with open(source, "rb") as image_file:
        image_bytes = image_file.read()

    extracted_text = extract_from_images_with_rapidocr([image_bytes])
    documents = [Document(page_content=extracted_text, metadata={"source": source})]
    return documents

def load_csv(source):
    loader = CSVLoader(file_path=source) 
    documents = loader.load()
    return documents

def loader(source):
    # Determine file type and process accordingly
    if source.lower().endswith(".pdf"):
        return load_pdf(source)
    elif source.lower().endswith((".png", ".jpg", ".jpeg")):
        return load_image(source)
    elif source.lower().endswith((".csv")):
        return load_csv(source)
    else:
        raise ValueError(f"Unsupported file type: {source}")
   
   