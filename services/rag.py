"""Retrieval-Augmented Generation (RAG) over user-uploaded documents.

Tech stack (all free + Streamlit-Cloud friendly, no heavy native wheels):

* Embeddings  -> Google Gemini ``text-embedding-004`` (free tier, API based,
  so nothing large is downloaded and it runs fine within Cloud's memory limit).
* Vector store -> LangChain ``InMemoryVectorStore`` (pure Python, per session).
* PDF parsing  -> ``pypdf`` (pure Python).

The embedding backend is the only part that needs a key: a free ``GOOGLE_API_KEY``
from https://aistudio.google.com/app/apikey.
"""

import io
import os

from langchain_core.documents import Document
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter

from utils.config import load_secrets

# Current GA Gemini embedding model. Override with the GOOGLE_EMBEDDING_MODEL
# env/secret if Google renames it (run list_embedding_models() to see options).
DEFAULT_EMBEDDING_MODEL = "models/gemini-embedding-001"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
DEFAULT_K = 4


def get_embeddings():
    """Return the Google Gemini embeddings client.

    Imported lazily so the rest of the app (and the test suite) does not need
    ``langchain-google-genai`` installed just to import this module.
    """
    from langchain_google_genai import GoogleGenerativeAIEmbeddings

    load_secrets()
    model = os.getenv("GOOGLE_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL)
    return GoogleGenerativeAIEmbeddings(
        model=model,
        google_api_key=os.getenv("GOOGLE_API_KEY"),
    )


def list_embedding_models():
    """Print Gemini models that support embeddings for the current API key.

    Handy for diagnosing "model not found" errors:
        python -c "from services.rag import list_embedding_models as f; f()"
    """
    import google.generativeai as genai

    load_secrets()
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    for m in genai.list_models():
        if "embedContent" in getattr(m, "supported_generation_methods", []):
            print(m.name)


def _read_file(uploaded_file):
    """Extract raw text from a Streamlit ``UploadedFile`` (PDF or plain text)."""
    name = uploaded_file.name.lower()
    data = uploaded_file.getvalue()

    if name.endswith(".pdf"):
        from pypdf import PdfReader

        reader = PdfReader(io.BytesIO(data))
        return "\n".join((page.extract_text() or "") for page in reader.pages)

    # .txt, .md, and anything else we treat as UTF-8 text.
    return data.decode("utf-8", errors="ignore")


def build_documents(files):
    """Turn uploaded files into chunked ``Document`` objects (no embeddings).

    Kept separate from embedding so it can be unit-tested without any API key.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    documents = []
    for uploaded_file in files:
        text = _read_file(uploaded_file)
        if not text.strip():
            continue
        for chunk in splitter.split_text(text):
            documents.append(
                Document(page_content=chunk, metadata={"source": uploaded_file.name})
            )

    return documents


def build_retriever_from_files(files, k=DEFAULT_K):
    """Read + chunk + embed uploaded files and return a retriever."""
    documents = build_documents(files)
    if not documents:
        raise ValueError("No readable text was found in the uploaded file(s).")

    store = InMemoryVectorStore(get_embeddings())
    store.add_documents(documents)
    return store.as_retriever(search_kwargs={"k": k})
