# app.py

from dotenv import load_dotenv
from src.document_processor import process_document
from src.rag_chain import create_rag_chain
import openlit

openlit.init(
    otlp_endpoint="http://127.0.0.1:4318"
)
load_dotenv()

def main():
    source = input("Enter the path to the document (PDF, csv, or image): ")
    documents = process_document(source)

    while True:
        question = input("Ask a question about the document (or type 'quit' to quit): ")
        if question.lower() == "quit":
            break

        # Create rag chain
        rag_chain = create_rag_chain(documents)
        answer = rag_chain.invoke(question)

        # # Print only the answer
        # answer_start_index = answer.find("Answer:")
        # answer_content = answer[answer_start_index:].strip()
        # print(answer_content)   

        print(f"\nAnswer:{answer}")

if __name__ == "__main__":
    main()