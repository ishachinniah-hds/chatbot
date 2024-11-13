# rag_chain.py

from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
# from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain.embeddings import HuggingFaceBgeEmbeddings
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

# Load the API key from env variables
load_dotenv()

RAG_PROMPT_TEMPLATE = """
You are a helpful coding assistant that can answer questions about the provided context. The context is usually a PDF document or an image (screenshot) of a code file. Augment your answers with code snippets from the context if necessary.

If you don't know the answer, say you don't know.

Context: {context}
Question: {question}
"""
PROMPT = PromptTemplate.from_template(RAG_PROMPT_TEMPLATE)


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def create_rag_chain(chunks):
    # Initialize Huggingface embeddings
    embeddings_model = "sentence-transformers/all-mpnet-base-v2"
    embeddings = HuggingFaceBgeEmbeddings(model_name=embeddings_model)

    # Set up Chroma vector store
    doc_search = Chroma.from_documents(chunks, embeddings)
    retriever = doc_search.as_retriever(
        search_type="mmr",
        search_kwargs={'k': 6, 'lambda_mult': 0.25}
    )
    # doc_search = FAISS.from_documents(chunks, embeddings)
    # retriever = doc_search.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    # Set up Huggingface language model
    llm_model = "meta-llama/Llama-3.2-3B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(llm_model)
    model = AutoModelForCausalLM.from_pretrained(llm_model)
    hf_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer, model_kwargs={"torch_dtype": torch.bfloat16}, device="cpu", max_new_tokens=256,)
    llm = HuggingFacePipeline(pipeline=hf_pipeline)

    # RAG chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | PROMPT
        | llm
        | StrOutputParser()
    )

    return rag_chain
