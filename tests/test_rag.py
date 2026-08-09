import pytest

from services.rag import build_documents, build_retriever_from_files


class FakeUploadedFile:
    """Minimal stand-in for a Streamlit UploadedFile."""

    def __init__(self, name, data: bytes):
        self.name = name
        self._data = data
        self.size = len(data)

    def getvalue(self):
        return self._data


def test_build_documents_from_text():
    text = b"LangGraph is a framework for building stateful agents. " * 100
    files = [FakeUploadedFile("notes.txt", text)]

    docs = build_documents(files)

    assert len(docs) >= 1
    assert all(d.metadata["source"] == "notes.txt" for d in docs)
    assert "LangGraph" in docs[0].page_content


def test_build_documents_skips_empty():
    files = [FakeUploadedFile("empty.txt", b"   ")]

    assert build_documents(files) == []


def test_retriever_finds_relevant_chunk():
    pytest.importorskip("rank_bm25")

    text = (
        b"Anubhav is a machine learning engineer. "
        b"He built a chatbot with LangGraph and Streamlit. "
        b"His favourite framework for retrieval is BM25. "
    ) * 20
    files = [FakeUploadedFile("resume.txt", text)]

    retriever = build_retriever_from_files(files, k=2)
    results = retriever.invoke("What framework is used for retrieval?")

    assert results
    assert any("BM25" in d.page_content for d in results)
