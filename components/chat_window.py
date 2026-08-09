import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage

from main import workflow
from services.rag import build_retriever_from_files
from services.vision import image_to_data_uri, is_image

BASE_SYSTEM_PROMPT = "You are a helpful assistant."

ATTACH_TYPES = ["png", "jpg", "jpeg", "webp", "pdf", "txt", "md"]


def _build_system_message(user_text):
    """Fold any relevant uploaded-document context into the system prompt.

    Retrieval happens here on Streamlit's main thread, where session_state is
    valid (unlike inside a LangGraph tool, which runs on a worker thread).
    """
    retriever = st.session_state.get("retriever")
    if retriever is None or not user_text:
        return SystemMessage(content=BASE_SYSTEM_PROMPT)

    try:
        docs = retriever.invoke(user_text)
    except Exception:
        docs = []

    if not docs:
        return SystemMessage(content=BASE_SYSTEM_PROMPT)

    context = "\n\n---\n\n".join(
        f"[source: {d.metadata.get('source', 'document')}]\n{d.page_content}"
        for d in docs
    )
    return SystemMessage(
        content=(
            BASE_SYSTEM_PROMPT
            + "\n\nThe user has uploaded documents. Use the context below to "
            "answer their question when relevant. If the answer is not in the "
            "context, say you could not find it in the documents.\n\n" + context
        )
    )


def _human_message(user_text, images):
    """Build a HumanMessage — multimodal (text + images) if any images attached."""
    if not images:
        return HumanMessage(content=user_text)

    content = [{"type": "text", "text": user_text or "Describe the attached image(s)."}]
    for image in images:
        content.append(
            {"type": "image_url", "image_url": {"url": image_to_data_uri(image)}}
        )
    return HumanMessage(content=content)


def _render_camera():
    """A ChatGPT-style camera: capture a photo, then send it with your message."""
    with st.expander("📷 Camera"):
        photo = st.camera_input("Take a photo", key="camera")
        if photo is not None:
            st.session_state["pending_image"] = photo
            st.caption("Photo captured — type a message and send to include it.")


def _display_text(user_text, images, docs):
    """What we store/show in history (never the raw base64 image bytes)."""
    parts = [user_text] if user_text else []
    if images:
        parts.append(f"_[{len(images)} image(s) attached]_")
    if docs:
        parts.append(f"_[{len(docs)} document(s) attached]_")
    return "\n\n".join(parts).strip()


def chat_window():
    for message in st.session_state["message_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    _render_camera()

    submission = st.chat_input(
        "Type here — use + to attach images or documents",
        accept_file="multiple",
        file_type=ATTACH_TYPES,
    )

    if not submission:
        return

    user_text = (submission.text or "").strip()
    files = list(submission.files or [])

    # Include a camera photo if one was captured this session.
    pending = st.session_state.pop("pending_image", None)
    if pending is not None:
        files.append(pending)

    images = [f for f in files if is_image(f)]
    docs = [f for f in files if not is_image(f)]

    # Index attached documents so RAG can answer about them.
    if docs:
        try:
            st.session_state["retriever"] = build_retriever_from_files(docs)
            st.session_state["rag_sources"] = [f.name for f in docs]
        except Exception as exc:
            st.error(f"Could not read attached document(s): {exc}")

    if not user_text and not images and not docs:
        return

    display = _display_text(user_text, images, docs)
    st.session_state["message_history"].append({"role": "user", "content": display})
    with st.chat_message("user"):
        st.markdown(display)

    # Documents-only submission: just confirm indexing, no model call.
    if not user_text and not images:
        note = f"Indexed {len(docs)} document(s). Ask me anything about them."
        with st.chat_message("assistant"):
            st.markdown(note)
        st.session_state["message_history"].append(
            {"role": "assistant", "content": note}
        )
        return

    system_message = _build_system_message(user_text)
    human_message = _human_message(user_text, images)

    config = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {"thread_id": st.session_state["thread_id"]},
        "run_name": "chat_trun",
    }

    with st.chat_message("assistant"):

        def response_generator():
            for message_chunk, metadata in workflow.stream(
                {"messages": [system_message, human_message]},
                config=config,
                stream_mode="messages",
            ):
                if metadata["langgraph_node"] == "chat_node":
                    yield message_chunk.content

        ai_message = st.write_stream(response_generator())

    st.session_state["message_history"].append(
        {"role": "assistant", "content": ai_message}
    )
