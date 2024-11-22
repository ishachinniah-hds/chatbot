# Simple RAG Application

This project is a simple Retrieval-Augmented Generation (RAG) application that allows users to query context within PDF or image files (JPEG, PNG, JPG) and recieve relevant context-based responses using local Large Language Models. The application utilizes Langchain framework, Huggingface transformer LLMs, ChromaDB vector search, and OpenLit AI monitoring.

The application was developed on **MacOS Sonoma 14.7.1** operating system using an **Apple M3 Pro** chip. 


## Project Capabilities

- **Document Querying**: Query PDFs and image files to get relevant information based on document context.
- **Local LLM Models**: Utilize `meta-llama/Llama-3.2-3B-Instruct` model from Hugging Face for response generation.
- **Vector Search**: Context retrieval using ChromaDB.
- **AI monitoring**: `OpenLit` tracks AI metrics for insights into the application usage and performance.


## Requirements
All required packages and dependencies can be installed:

```bash
pip install -r requirements.txt
```


## Environment Setup
Users must be registered with [Hugging Face](https://huggingface.co/) and generate an API token. The application requires the Hugging Face CLI for API key management and model access:

### Huggingface CLI
```bash
pip install huggingface-hub
huggingface-cli login
```
After logging in, enter your Hugging Face API key when prompted.  

### Environemnt Variable
Alternatively, you can set the environment variable for the Hugging Face API key manually in the `.env` file.


## Model access
Models used in this application may require access permission to be granted by the developer - for instance, Meta llama models require permissions access from Meta. Access requests can be made within [Hugging Face models](https://huggingface.co/models) by filling out the Community License Agreement form under the specific model. Once permission is granted, the model is automatically made available through the Hugging Face CLI login.

### Supported Models 

| 🤖 Model                                   | Supported | Access Request | Link to the model                                                                                                                                          |
|--------------------------------------------|-----------|------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `meta-llama/Llama-3.1-8B-Instruct`          | ✅         | Meta         | [link](https://huggingface.co/meta-llama/Llama-3.2-3B-Instruct)                                                                       |
| `meta-llama/Llama-2-7b-chat-hf`              | ✅         | Meta         | [link](https://huggingface.co/meta-llama/Llama-2-7b-chat-hf)                                                                                               


## Codebase Structure
- `src/document_processor.py`: Manages document loading and processing fo a CSV, PDF, or image files.
- `src/text_split.py`: Splits the document into chunks of text.
- `src/vector_store.py`: Embeds the document chunks into a ChromaDB vector database and returns a retriever.
- `src/prompt.py`: Generates a prompt template to combine the relevant context and user query.
- `src/rag_chain.py`: Creates the RAG chain by feeding the user query and relevant context to the LLM.
- `app.py`: The CLI interface for user interaction - inputting documents and querying the RAG assistant.


## Monitoring with OpenLit
The Project integrates [OpenLit](https://github.com/openlit/openlit) to get insights into the AI application's performance, behavior, and identify areas for improvement. The openlit SDK installation and initialization is completed within the app.py file and requirement.txt file. The following steps are required to deploy and visualize the OpenLit Stack:

### Deploy OpenLIT Stack
Git Clone OpenLIT Repository
```
git clone https://github.com/openlit/openlit.git
```
Run the following command within the Openlit directory:
```
docker compose up -d
```
### OpenLit Dashboard
To visualize the observability data being collected and sent to OpenLit, enter 127.0.0.1:3000 on your browser and login using the following default credentials: <br/>
Email: user@openlit.io <br/>
Password: openlituser


## Running the Application
The application can be run through the CLI by executing the command `python app.py` within the chatbot directory. The application will request the user to input the file path to the document that will be queried, followed by a question about the uploaded document. The RAG application will process the document and output relevant context-based answers about the document using the LLM. 


