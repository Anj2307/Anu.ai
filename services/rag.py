"""Retrieval-Augmented Generation (RAG) over user-uploaded documents.

Uses BM25 keyword retrieval, so the whole feature is free, needs **no API key
and no external service**, and installs cleanly on Streamlit Cloud / Python 3.14
(every dependency is pure Python):

* Text extraction -> ``pypdf`` (PDF) / UTF-8 decode (txt, md)
* Chunking        -> LangChain ``RecursiveCharacterTextSplitter``
* Retrieval       -> ``BM25Retriever`` (``rank_bm25``) — lexical / keyword match

Trade-off vs. embedding-based RAG: BM25 matches on shared words rather than
meaning, so it is great for names, terms and facts (resumes, notes, docs) but
weaker at synonyms/paraphrase. It is the most reliable free option here.
"""

import io

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
DEFAULT_K = 4


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
    """Turn uploaded files into chunked ``Document`` objects.

    Kept separate from retriever construction so it can be unit-tested without
    ``rank_bm25`` installed.
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
    """Read + chunk uploaded files and return a BM25 keyword retriever."""
    documents = build_documents(files)
    if not documents:
        raise ValueError("No readable text was found in the uploaded file(s).")

    # Imported lazily so importing this module does not require rank_bm25.
    from langchain_community.retrievers import BM25Retriever

    retriever = BM25Retriever.from_documents(documents)
    retriever.k = k
    return retriever
