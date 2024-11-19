# app.py

from dotenv import load_dotenv
from src.document_processor import process_document
from src.rag_chain import create_rag_chain
import openlit

from transformers import AutoTokenizer

openlit.init(
    otlp_endpoint="http://127.0.0.1:4318"
)
load_dotenv()

    # # Set up Huggingface language model
    # llm_model = "meta-llama/Llama-3.2-3B-Instruct"
    # tokenizer = AutoTokenizer.from_pretrained(llm_model)

    # # Number of prompt tokens
    # encoded_text = tokenizer(result, return_tensors="pt")
    # token_count = len(encoded_text["input_ids"][0]) 
    # print(f"Result token count: {token_count}") 

def main():
    source = input("Enter the path to the document (PDF, csv, or image): ")
    documents = process_document(source)

    while True:
        question = input("Ask a question about the document (or type 'exit' to quit): ")
        if question.lower() == "exit":
            break

        # Create rag chain
        rag_chain = create_rag_chain(documents)
        answer = rag_chain.invoke(question)
        print("Answer:", answer)

if __name__ == "__main__":
    main()