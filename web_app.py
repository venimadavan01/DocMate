from flask import Flask, render_template, request, jsonify
import os
import shutil

# Import ingestion and RAG pipeline components
from ingest import ingest, load_document, split_documents, create_vector_store
from rag_pipeline import load_vector_store, get_retriever, create_llm, generate_answer
from utils import format_sources

import warnings
warnings.filterwarnings("ignore")  # Suppress warnings for cleaner console output


# --------------------------------------------------
# FLASK APP INITIALIZATION
# --------------------------------------------------
app = Flask(__name__)

# Directory to store uploaded files
UPLOAD_FOLDER = "data"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Global objects for vector DB, retriever, and LLM
db = None
retriever = None
llm = create_llm()  # Initialize LLM once for reuse


# --------------------------------------------------
# HOME ROUTE
# --------------------------------------------------
# Renders the main UI page
@app.route("/")
def index():
    return render_template("index.html")


# --------------------------------------------------
# FILE UPLOAD & INGESTION ROUTE
# --------------------------------------------------
# Handles:
# 1. File upload
# 2. Document loading
# 3. Chunking
# 4. Vector DB creation
# 5. Retriever initialization
@app.route("/upload", methods=["POST"])
def upload():
    global retriever

    # Get uploaded files
    files = request.files.getlist("files")

    # STEP 1: Reset existing vector database
    if os.path.exists("vectorstore"):
        shutil.rmtree("vectorstore")
        print("Old vectorstore deleted")

    # STEP 2: Initialize document container
    all_docs = []

    # STEP 3: Load each uploaded file
    for file in files:
        path = os.path.join("data", file.filename)
        file.save(path)

        print("Saving file to:", path)

        # Load document using appropriate loader
        docs = load_document(path)
        print(f"{file.filename} → pages:", len(docs))

        # Append loaded documents
        all_docs.extend(docs)

        # Debug check
        print("FILE EXISTS:", os.path.exists(path))

    print("DOCS LOADED:", len(all_docs))

    # STEP 4: Split documents into chunks
    chunks = split_documents(all_docs)
    print("CHUNKS CREATED:", len(chunks))

    # STEP 5: Create vector database (embeddings + storage)
    create_vector_store(chunks)
    print("Vectorstore created")

    # STEP 6: Initialize retriever for query handling
    retriever = get_retriever()

    return jsonify({"message": "Upload successful"})


# --------------------------------------------------
# QUESTION ANSWERING ROUTE (RAG)
# --------------------------------------------------
# Handles:
# 1. User query
# 2. Retrieval of relevant chunks
# 3. LLM-based answer generation
# 4. Source formatting
@app.route("/ask", methods=["POST"])
def ask():

    # Extract query from request
    query = request.json.get("query")

    # Generate answer using RAG pipeline
    answer, docs = generate_answer(query, retriever, llm)

    # Save interaction for logging / evaluation
    with open("v1/sample_output.txt", "a", encoding="utf-8") as f:
        f.write(f"\nUser: {query}\nSystem: {answer}\n{'-'*40}\n")

    # Format sources for UI display
    sources = format_sources(docs)

    # Debug logs for verification
    print("QUERY:", query)
    print("RETRIEVED DOCS:", len(docs))

    for d in docs:
        print("DOC:", d.page_content[:200])

    # Return response to frontend
    return jsonify({
        "answer": answer,
        "sources": sources
    })


# --------------------------------------------------
# APPLICATION ENTRY POINT
# --------------------------------------------------
# Runs Flask app in debug mode (without auto-reloader issues)
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)