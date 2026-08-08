import os


def load_secrets():
    """Bridge Streamlit secrets into environment variables.

    Works in every environment we care about:

    * Local development  -> keys come from a ``.env`` file (loaded via dotenv).
    * Streamlit Cloud    -> keys are entered in the app's *Secrets* panel and
      exposed through ``st.secrets``; here we copy them into ``os.environ`` so
      libraries that read env vars directly (LangChain, Tavily, OpenAI) work.

    Environment variables that are already set always win, so a local ``.env``
    is never overwritten. The call is safe to run when no secrets exist.
    """
    try:
        import streamlit as st

        for key in st.secrets:
            value = st.secrets[key]
            if isinstance(value, str) and not os.environ.get(key):
                os.environ[key] = value
    except Exception:
        # No secrets file / not running under Streamlit -> rely on env / .env.
        pass
