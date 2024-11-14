# Simple RAG Application

This project is a simple Retrieval-Augmented Generation (RAG) application that allows users to query context within PDF or image files (JPEG, PNG, JPG) and recieve relevant context-based responses using local Large Language Models. The application utilizes Langchain framework, Huggingface transformer LLMs, ChromaDB vector search, and OpenLit AI monitoring.

The application was developed on **MacOS Sonoma 14.7.1** 


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
Alternatively, you can set the environment variable for the Hugging Face API key manually in the .env file.


## Llama3 model access
The `meta-llama/Llama-3.1-8B-Instruct` model used in this application requires access permission to be granted by Meta. Access requests can be made under the [llama3 model](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct) on the Hugging Face webpage by filling out the Meta Release form. Once permission is granted, the model is automatically made available though you Hugging Face CLI login.


## Codebase Structure
- `src/document_processor.py`: Manages document loading, processing, and splitting gor PDF and image files.
- `src/rag_chain.py`: Creates the RAG chain using embeddings vector databsase and LLM calls.
- `app.py`: The CLI interface for user interaction, processing input documents, and querying the RAG assistant.


## Monitoring with OpenLit
The Project integrates OpenLit to track AI metrics during application usage.... (should users compose docker again?)




### OpenTelemetry Collector Core Distro

This distribution contains all the components from the [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector) repository and a small selection of components tied to open source projects from the [OpenTelemetry Collector Contrib](https://github.com/open-telemetry/opentelemetry-collector-contrib) repository.

This distribution is considered "classic" and is no longer accepting new components outside of components from the Core repo.

#### Components

The full list of components is available in the [manifest](manifest.yaml)

##### Rules for Component Inclusion

Since Core is a "classic" distribution its components are strictly limited to what currently exists in its [manifest](manifest.yaml) and any future components in Core.
No other components from Contrib should be added.
