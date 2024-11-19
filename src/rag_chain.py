# rag_chain.py

from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch
from src.vector_store import create_vector_store
from src.split import split_documents

# Load the API key from env variables
load_dotenv()

RAG_PROMPT_TEMPLATE = """
You are a helpful assistant that can answer questions about the provided context.

If you don't know the answer, say you don't know.

Context: {context}
Question: {question}
"""
PROMPT = PromptTemplate.from_template(RAG_PROMPT_TEMPLATE)

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def create_rag_chain(documents):
    # Split and embed the documents
    chunks = split_documents(documents)
    retriever = create_vector_store(chunks)

    # Set up Huggingface language model
    llm_model = "meta-llama/Llama-3.2-3B-Instruct"
    tokenizer = AutoTokenizer.from_pretrained(llm_model)
    model = AutoModelForCausalLM.from_pretrained(llm_model)

    hf_pipeline = pipeline(
        "text-generation", 
        model=model, 
        tokenizer=tokenizer, 
        model_kwargs={"torch_dtype": torch.bfloat16}, 
        device=torch.device('cuda' if torch.cuda.is_available() else 'cpu'),
        pad_token_id=tokenizer.eos_token_id,
        max_new_tokens=256, 
        )
    llm = HuggingFacePipeline(pipeline=hf_pipeline)

    # RAG chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | PROMPT
        | llm
        | StrOutputParser()
    )

    return rag_chain
