# app.py

from dotenv import load_dotenv
from src.load_document import loader
from src.rag_chain import create_rag_chain
from src.text_split import split_documents
from src.vector_store import create_vector_store
from src.prompt import create_prompt
import openlit

openlit.init(
    otlp_endpoint="http://127.0.0.1:4318"
)
load_dotenv()

def main():
    # set parameters - currently hard coded, should read json file
    filepath = "/Users/isha/Desktop/Documents/movies_processed.csv"
    question = "What is a good animated movie similar to Aladdin?"
    chunk_size = 1000
    chunk_overlap = 200
    embedding_model="sentence-transformers/all-mpnet-base-v2"
    llm_model="meta-llama/Llama-3.2-3B-Instruct"
    template = """
You are a helpful movie recommender system that uses the available information from a dataset to provide insightful and relevant recommendations. Here are a few examples of movie recommendations: 
 
Example 1: 
Question: What movie would you recommend for someone who enjoys an action thriller movie? 
Answer: I would recommend 'Missing Impossible' - a high-energy action, adventure, and thriller film.  
The plot follows CIA agent Ethan Hunt, who must clear his name after being suspected of being a mole within the agency.  
It's a thrilling experience, widely favored by action movie fans. 
 
Example 2:  
Question: Can you recommend 5 movies to watch for someone who enjoyed Star Wars? 
Answer: I would recommend the following five movies, which share similar themes of action, adventure, and science fiction: ‘Independence Day’, ‘Stargate’, ‘Escape from L.A.’, ‘Johnny Mnemonic’, and ‘RoboCop 3’.  
These films are popular among fans of thrilling, futuristic adventures and action-packed sci-fi stories. 
 
Now based on the context below, provide a movie recommendation: 
 
Context: {context} 
Question: {question} 
"""

    # call files to load, chunk, embed, create prompt, set up rag chain, invoke rag chain
    documents = loader(filepath)
    chunks = split_documents(documents, chunk_size, chunk_overlap)
    retriever = create_vector_store(chunks, embedding_model)
    prompt = create_prompt(template)
    rag_chain = create_rag_chain(retriever, llm_model, prompt)
    answer = rag_chain.invoke(question)
    print(f"\nAnswer:{answer}")

    # # Print only the answer
    # answer_start_index = answer.find("Answer:")
    # answer_content = answer[answer_start_index:].strip()
    # print(answer_content) 

if __name__ == "__main__":
    main()