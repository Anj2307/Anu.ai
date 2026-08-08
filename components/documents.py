import streamlit as st

from services.rag import build_retriever_from_files


def render_document_uploader():
    """Sidebar knowledge-base uploader.

    Lets the user attach PDF / text files. On "Build", the files are chunked,
    embedded and stored as a retriever in ``st.session_state`` so the
    ``search_documents`` tool can query them during the chat.
    """
    st.sidebar.header("📄 Knowledge Base")

    files = st.sidebar.file_uploader(
        "Upload documents",
        type=["pdf", "txt", "md"],
        accept_multiple_files=True,
        key="rag_uploader",
    )

    if st.sidebar.button("Build knowledge base"):
        if not files:
            st.sidebar.warning("Upload at least one file first.")
        else:
            try:
                with st.spinner("Indexing documents…"):
                    st.session_state["retriever"] = build_retriever_from_files(files)
                st.sidebar.success(f"Indexed {len(files)} file(s). Ask me about them!")
            except Exception as exc:  # surface a friendly error, keep app alive
                st.sidebar.error(f"Could not index documents: {exc}")

    if st.session_state.get("retriever") is not None:
        st.sidebar.caption("✅ Knowledge base ready")
