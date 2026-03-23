# DocMate -- Intelligent Document Q&A System (RAG)

## Assignment Overview

This project implements an **Intelligent Document Question-Answering System** using **Retrieval-Augmented Generation (RAG)** and open-source
Large Language Models (LLMs).

The system allows users to upload documents and ask natural language questions, receiving accurate, context-aware answers with source references.

------------------------------------------------------------------------

## Objective

-   Ingest and process documents (PDF, TXT, DOCX)
-   Answer user queries using document content
-   Provide source attribution (page/document reference)
-   Demonstrate prompt engineering and LLM integration

------------------------------------------------------------------------

## Functional Requirements

-   Supports document upload (PDF, TXT, DOCX)
-   Enables natural language question answering
-   Provides source attribution
-   Interactive web-based UI (Flask + Bootstrap)

------------------------------------------------------------------------

## Technical Stack

-   Python
-   Flask
-   LangChain
-   ChromaDB
-   Sentence Transformers
-   Ollama (Llama3)

------------------------------------------------------------------------

## RAG Architecture

User Query → Retriever → Relevant Chunks → LLM → Answer + Sources

### Pipeline Flow

1.  Upload document
2.  Split into chunks
3.  Generate embeddings
4.  Store in vector DB
5.  Retrieve relevant chunks
6.  Generate answer using LLM

------------------------------------------------------------------------

## Project Structure

DOCMATE/ ├── data/ ├── static/ │ └── styles.css ├── templates/ │ └──
index.html ├── vectorstore/ ├── embeddings.py ├── ingest.py ├──
rag_pipeline.py ├── utils.py ├── web_app.py ├── requirements.txt ├──
sample_output.txt ├── README.md

------------------------------------------------------------------------

## Setup Instructions

### 1. Clone Repository

git clone `<repo-url>`{=html} cd DOCMATE

### 2. Create Virtual Environment

python -m venv docenv docenv`\Scripts`{=tex}`\activate`{=tex}

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Run Ollama

ollama run phi3

### 5. Run App

python web_app.py

Open: http://127.0.0.1:5000

------------------------------------------------------------------------

## Example Usage

User: What are the main topics covered?

System: - Provides structured answer - Uses document context - Includes
sources

------------------------------------------------------------------------

## Source Attribution

-   Displays page number
-   Shows source document
-   Ensures transparency

------------------------------------------------------------------------

## Performance Optimization

-   Chunk size: 300
-   Retrieval: k=2
-   Shared embeddings
-   Lightweight models (phi3)

------------------------------------------------------------------------

## Limitations

-   No image/table extraction
-   DOC format not supported
-   Depends on document quality

------------------------------------------------------------------------

## Future Enhancements

-   Conversation memory
-   Multi-language support
-   UI improvements
-   Re-ranking

------------------------------------------------------------------------

## Final Statement

Studymate is a modular RAG-based system that provides accurate,
context-aware answers with source attribution using open-source LLMs.

------------------------------------------------------------------------

## Author

Developed as part of a Generative AI assignment.
