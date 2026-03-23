from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from embeddings import embeddings
import os
import warnings

# Suppress unnecessary warnings for cleaner logs
warnings.filterwarnings("ignore")


# --------------------------------------------------
# DOCUMENT LOADING
# --------------------------------------------------
# Loads documents based on file type (PDF / TXT)
# Performs encoding handling for TXT files
def load_document(file_path):
    print("LOADING FILE:", file_path)

    # Validate file existence
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")

    try:
        # Handle PDF files
        if file_path.lower().endswith(".pdf"):
            loader = PyPDFLoader(file_path)

        # Handle TXT files with encoding fallback
        elif file_path.lower().endswith(".txt"):
            try:
                loader = TextLoader(file_path, encoding="utf-8", autodetect_encoding=True)
                return loader.load()
            except:
                loader = TextLoader(file_path, encoding="latin-1")
                return loader.load()

        # Unsupported formats
        else:
            raise ValueError("Unsupported file format")

        # Load documents
        docs = loader.load()

        print("PAGES LOADED:", len(docs))
        return docs

    # Standardized error for UI
    except ValueError as ve:
        raise ValueError("Unsupported file format. Please upload PDF, TXT, or DOCX.")

    # Catch-all for unexpected issues
    except Exception as e:
        print("ERROR IN LOADING:", str(e))
        raise e


# --------------------------------------------------
# DOCUMENT SPLITTING
# --------------------------------------------------
# Splits documents into smaller chunks for better retrieval
# Smaller chunks improve embedding accuracy and retrieval speed
def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        # chunk_size=500,
        # chunk_overlap=100
        chunk_size=300,
        chunk_overlap=30
    )
    return splitter.split_documents(documents)


# --------------------------------------------------
# VECTOR STORE CREATION
# --------------------------------------------------
# Converts text chunks into embeddings and stores them in ChromaDB
# Enables semantic search for RAG pipeline
def create_vector_store(chunks):
    db = Chroma.from_documents(
        chunks,
        embedding=embeddings,
        persist_directory="vectorstore"
    )

    # Duplicate call (retained as per original code)
    db = Chroma.from_documents(
        chunks,
        embedding=embeddings,
        persist_directory="vectorstore"
    )

    # Persist database to disk
    db.persist()

    return db


# --------------------------------------------------
# INGESTION PIPELINE
# --------------------------------------------------
# End-to-end pipeline:
# Load → Split → Embed → Store
def ingest(file_path):
    print("Loading document...")
    docs = load_document(file_path)

    print("Splitting document...")
    chunks = split_documents(docs)

    print("Creating vector DB...")
    db = create_vector_store(chunks)

    print("Ingestion complete.")
    return db