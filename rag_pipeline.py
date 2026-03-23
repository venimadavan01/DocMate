import warnings
warnings.filterwarnings("ignore")  # Suppress unnecessary warnings for cleaner output


from langchain_community.vectorstores import Chroma
# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM

from embeddings import embeddings


# --------------------------------------------------
# LOAD EXISTING VECTOR STORE
# --------------------------------------------------
# Loads a persisted ChromaDB vector store from disk
# Used when we want to reuse previously stored embeddings
def load_vector_store():
    
    return Chroma(
        persist_directory="v1/vectorstore",
        embedding_function=embeddings
    )


# --------------------------------------------------
# RETRIEVER SETUP
# --------------------------------------------------
# Creates a retriever from the vector store
# Responsible for fetching top-k relevant chunks for a query
def get_retriever():

    db = Chroma(
        persist_directory="vectorstore",
        embedding_function=embeddings
    )

    # k=2 → faster, smaller context (optimized for performance)
    return db.as_retriever(search_kwargs={"k": 2})

    # Alternative (higher recall but slower)
    # return db.as_retriever(search_kwargs={"k": 3})


# --------------------------------------------------
# LLM INITIALIZATION
# --------------------------------------------------
# Initializes the local LLM using Ollama
# Model can be switched (llama3, mistral, phi3) for performance tuning
def create_llm():
    return OllamaLLM(model="llama3")  
    # Optional tuning:
    # temperature=0 → deterministic output
    # num_predict=200 → shorter responses
    # models: phi3 (fast), mistral (balanced)


# --------------------------------------------------
# ANSWER GENERATION (RAG CORE)
# --------------------------------------------------
# Pipeline:
# 1. Retrieve relevant chunks
# 2. Build context
# 3. Construct prompt
# 4. Generate response using LLM
def generate_answer(query, retriever, llm):

    # Retrieve relevant documents
    docs = retriever.invoke(query)

    # Combine retrieved chunks into a single context
    context = "\n\n".join([doc.page_content for doc in docs])

    # Debug: print partial context for verification
    print("CONTEXT:", context[:500])

    # Prompt engineering to guide structured output
    prompt = f"""
Answer the question using the context below.

Format your answer:
- Use bullet points where appropriate
- Keep sentences clear and short
- Add spacing between points
- Avoid long paragraphs

Context:
{context}

Question:
{query}

Answer:
"""

    # Generate response using LLM
    response = llm.invoke(prompt)

    # Return both answer and source documents (for citation)
    return response, docs