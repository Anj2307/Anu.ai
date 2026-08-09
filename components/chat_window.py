import streamlit as st
from langchain_core.messages import HumanMessage, SystemMessage

from main import workflow

BASE_SYSTEM_PROMPT = "You are a helpful assistant."


def _build_system_message(user_input):
    """Build the system message, folding in any relevant uploaded-document context.

    Retrieval happens here, on Streamlit's main script thread, where
    ``st.session_state`` is valid — unlike inside a LangGraph tool, which runs
    on a worker thread with no session context.
    """
    retriever = st.session_state.get("retriever")
    if retriever is None:
        return SystemMessage(content=BASE_SYSTEM_PROMPT)

    try:
        docs = retriever.invoke(user_input)
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


def chat_window():
    for message in st.session_state["message_history"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Type here")

    if user_input:

        st.session_state["message_history"].append(
            {"role": "user", "content": user_input}
        )

        with st.chat_message("user"):
            st.markdown(user_input)

        system_message = _build_system_message(user_input)

        config = {
            "configurable": {"thread_id": st.session_state["thread_id"]},
            "metadata": {"thread_id": st.session_state["thread_id"]},
            "run_name": "chat_trun",
        }

        with st.chat_message("assistant"):

            def response_generator():
                for message_chunk, metadata in workflow.stream(
                    {"messages": [system_message, HumanMessage(content=user_input)]},
                    config=config,
                    stream_mode="messages",
                ):
                    if metadata["langgraph_node"] == "chat_node":
                        yield message_chunk.content

            ai_message = st.write_stream(response_generator())

        st.session_state["message_history"].append(
            {"role": "assistant", "content": ai_message}
        )
