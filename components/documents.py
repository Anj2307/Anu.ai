import streamlit as st

from services.rag import build_retriever_from_files


def _signature(files):
    """A cheap fingerprint of the uploaded file set to detect changes."""
    return tuple((f.name, f.size) for f in files) if files else ()


def render_document_uploader():
    """Sidebar knowledge-base uploader.

    Files are indexed automatically as soon as they are uploaded (no separate
    button), and the resulting BM25 retriever is stored in ``st.session_state``
    so the ``search_documents`` tool can query it during the chat.
    """
    st.sidebar.header("📄 Knowledge Base")

    files = st.sidebar.file_uploader(
        "Upload documents (PDF, TXT, MD)",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True,
        key="rag_uploader",
    )

    signature = _signature(files)

    # Only (re)build when the set of uploaded files actually changes.
    if signature != st.session_state.get("rag_signature"):
        if files:
            try:
                with st.spinner("Indexing documents…"):
                    st.session_state["retriever"] = build_retriever_from_files(files)
                st.session_state["rag_sources"] = [f.name for f in files]
            except Exception as exc:  # keep the app alive, show a friendly error
                st.session_state["retriever"] = None
                st.session_state["rag_sources"] = []
                st.sidebar.error(f"Could not index documents: {exc}")
        else:
            st.session_state["retriever"] = None
            st.session_state["rag_sources"] = []

        st.session_state["rag_signature"] = signature

    if st.session_state.get("retriever") is not None:
        sources = ", ".join(st.session_state.get("rag_sources", []))
        st.sidebar.success(f"✅ Indexed: {sources}")
    else:
        st.sidebar.caption("Upload a file and the chatbot can read it.")
