from services.rag import build_documents


class FakeUploadedFile:
    """Minimal stand-in for a Streamlit UploadedFile."""

    def __init__(self, name, data: bytes):
        self.name = name
        self._data = data

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
