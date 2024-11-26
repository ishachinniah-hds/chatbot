# app.py

import argparse
import json
from dotenv import load_dotenv
from src.load_document import loader
from src.rag_chain import create_rag_chain
from src.split_text import split_documents
from src.vector_store import create_vector_store
from src.prompt import create_prompt
import openlit

openlit.init(
    otlp_endpoint="http://127.0.0.1:4318"
)
load_dotenv()

def load_config(config_file):
    """
    Load the configuration parameters from a JSON file.
    """
    try:
        with open(config_file, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Config file {config_file} not found.")
    except json.JSONDecodeError:
        raise ValueError(f"Error decoding JSON from {config_file}. Ensure the file is properly formatted.")

def main():
    # Take a JSON file through comman-line argument
    parser = argparse.ArgumentParser(description="Process a JSON file")
    parser.add_argument('json_file', type=str, help='Path to the JSON file')
    args = parser.parse_args()

    # Load configuration from the JSON file
    config = load_config(args.json_file)

    # Use .get() method to extract parameters, providing sensible defaults
    filepath = config.get("filepath", "/Users/isha/desktop/Documents/movies_processed.csv")
    question = config.get("question", "What is a good animated movie similar to Aladdin?")
    chunk_size = config.get("chunk_size", 1000)
    chunk_overlap = config.get("chunk_overlap", 200)
    embedding_model = config.get("embedding_model", "sentence-transformers/all-mpnet-base-v2")
    llm_model = config.get("llm_model", "meta-llama/Llama-3.2-3B-Instruct")
    template = config.get("template", "Context: {context} Question: {question}")

    # call modules to load, chunk, embed, create prompt, set up rag chain, invoke rag chain
    documents = loader(filepath)
    chunks = split_documents(documents, chunk_size, chunk_overlap)
    retriever = create_vector_store(chunks, embedding_model)
    prompt = create_prompt(template)
    rag_chain = create_rag_chain(retriever, llm_model, prompt)
    answer = rag_chain.invoke(question)
    print(f"\nAnswer:\n{answer}")

    # # Print only the answer
    # answer_start_index = answer.find("Answer:")
    # answer_content = answer[answer_start_index:].strip()
    # print(answer_content) 

if __name__ == "__main__":
    main()