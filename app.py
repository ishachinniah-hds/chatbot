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
    # openlit dashboard endpoint
    # otlp_endpoint="http://127.0.0.1:4318"

    # elastic endpoint
    otlp_endpoint="https://my-observability-project-c7c032.apm.us-west-2.aws.elastic.cloud:443", 
    otlp_headers="Authorization=ApiKey cGV1TWlKTUJ0OUZSTkwxZU1Pbi06VS12WEpMd2FRMGFvSnF6WmxFcEJRZw=="
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
    # Take a JSON file through command-line argument
    parser = argparse.ArgumentParser(description="Process a JSON file")
    parser.add_argument('json_file', type=str, help='Path to the JSON file')
    args = parser.parse_args()

    # Load configuration from the JSON file
    config = load_config(args.json_file)

    # Use .get() method to extract parameters and provide default values    
    filepath = config.get("dataset_filepath", "./dataset/movies.csv")
    question = config.get("query", "What is a good animated movie similar to Aladdin?")
    chunk_size = config.get("chunk_size", 1000)
    chunk_overlap = config.get("chunk_overlap", 200)
    embedding_model = config.get("embedding_model", "sentence-transformers/all-mpnet-base-v2")
    llm_model = config.get("llm_model", "meta-llama/Llama-3.2-3B-Instruct")
    template = config.get("prompt_template", "Context: {context} Question: {question}")
    max_tokens = config.get("max_tokens", 256)
    temperature = config.get("temperature", 0.1)

    # call modules to load, chunk, embed, create prompt, set up rag chain, invoke rag chain
    documents = loader(filepath)
    chunks = split_documents(documents, chunk_size, chunk_overlap)
    retriever = create_vector_store(chunks, embedding_model)
    prompt = create_prompt(template)
    rag_chain = create_rag_chain(retriever, llm_model, prompt, max_tokens, temperature)
    answer = rag_chain.invoke(question)

    with open("output.txt", "w") as file:
        file.write(answer)
    print(f"\nOutput:\n{answer}")

if __name__ == "__main__":
    main()