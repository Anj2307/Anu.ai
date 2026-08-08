import streamlit as st


def require_login():
    """Gate the whole app behind a simple username.

    There is no password: whatever username is entered becomes that person's
    private namespace. The same username (on any device) sees the same chats,
    and a different username sees a different, isolated set of chats.

    Call this at the very top of the app, before anything reads ``user_id``.
    """
    if st.session_state.get("user_id"):
        return

    st.title("LangGraph Chatbot")
    st.subheader("Enter a username to continue")

    with st.form("login_form"):
        username = st.text_input("Username", placeholder="e.g. anubhav")
        submitted = st.form_submit_button("Continue")

    if submitted:
        cleaned = username.strip()
        if cleaned:
            st.session_state["user_id"] = cleaned
            st.rerun()
        else:
            st.error("Please enter a username.")

    # Stop here so the rest of the app never runs until a username is set.
    st.stop()


def logout():
    """Clear the session so the login screen is shown again."""
    for key in ("user_id", "message_history", "thread_id", "chat_threads"):
        st.session_state.pop(key, None)
    st.rerun()
