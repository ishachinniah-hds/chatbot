# app.py

from dotenv import load_dotenv
from src.document_processor import process_document
from src.rag_chain import create_rag_chain, format_docs
import openlit

openlit.init(
    otlp_endpoint="http://127.0.0.1:4318"
)
load_dotenv()

def main():
    # Get user input
    source = input("Enter the path to the document (PDF or image): ")
    question = input("Ask a question about the document (or type 'exit' to quit): ")
    
    # Process the document
    try:
        chunks = process_document(source)
        # with open("output.txt", "w") as file:
        #     print(chunks, file=file)
    except ValueError as e:
        print(f"Error processing document: {e}")
        return
    
    # Create RAG chain
    rag_chain = create_rag_chain(chunks)

    # Run the chain with the question 
    result = rag_chain.invoke(question)
    
    # Output the result
    print("RAG output: ")
    print(result)
    
if __name__ == "__main__":
    print("starting app.py main()")
    main()
