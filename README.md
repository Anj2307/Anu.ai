# Anu.ai — LangGraph Chatbot

A Streamlit chat app built on LangGraph with an intent router, tool calling
(calculator + Tavily web search), automatic chat titles, and SQLite-based
conversation persistence.

## Run locally

```bash
pip install -r requirements.txt
```

Create `.streamlit/secrets.toml` (copy from `.streamlit/secrets.toml.example`)
or a `.env` file with:

```toml
OPENROUTER_API_KEY = "sk-or-..."
TAVILY_API_KEY = "tvly-..."
```

Then start the app:

```bash
streamlit run app.py
```

## Deploy to Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to <https://share.streamlit.io> and click **Create app** → **Deploy a
   public app from GitHub**.
3. Select this repo/branch and set the **Main file path** to `app.py`.
4. Open **Advanced settings → Secrets** and paste:

   ```toml
   OPENROUTER_API_KEY = "sk-or-..."
   TAVILY_API_KEY = "tvly-..."
   ```

5. Click **Deploy**.

### Notes

- Secrets set in the dashboard are read by the app via `st.secrets` and bridged
  into environment variables (see `utils/config.py`), so LangChain / OpenAI /
  Tavily pick them up automatically.
- The SQLite database (`chatbot.db`) lives on Cloud's **ephemeral** filesystem —
  conversation history resets whenever the app restarts. Set `CHATBOT_DB_PATH`
  to relocate it if needed. For durable history, use an external database.
- `requirements.txt` must stay UTF-8 encoded. Do not overwrite it with a raw
  `pip freeze` on Windows PowerShell (`>` produces UTF-16, which breaks the
  Cloud build).
