# rag_chain.py

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def create_rag_chain(retriever, model_name, prompt):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(model_name)

    hf_pipeline = pipeline(
        "text-generation", 
        model=model, 
        tokenizer=tokenizer, 
        model_kwargs={"torch_dtype": torch.bfloat16}, 
        device=torch.device('cuda' if torch.cuda.is_available() else 'cpu'),
        pad_token_id=tokenizer.eos_token_id,
        max_new_tokens=256, 
        temperature = 0.5,
        )
    llm = HuggingFacePipeline(pipeline=hf_pipeline)

    # RAG chain
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain
