# SingleAgent Chatbot

A minimal stateful chatbot built on **langgraph** + **langchain_ollama**, with both **CLI** and **FastAPI** modes.

The app maintains conversation history in a local SQLite file (`chat_history.db`) and supports multiple sessions via `thread_id`.

---

## ✅ What this repo contains

- `graph_app.py` – core chat graph + state persistence (shared by CLI and FastAPI)
- `main.py` – simple FastAPI wrapper around `graph_app` (optional entrypoint)
- `SingleAgent.py` – legacy example (still works but superseded by `graph_app.py`)
- `chat_history.db` – generated at runtime; stores conversation history per `thread_id`

---

## 📦 Requirements

- Python 3.10+
- `ollama` installed & running
- A local Ollama model available (e.g., `qwen2.5-coder:7b`)

Python packages:

- `langgraph`
- `langchain_ollama`
- `fastapi` (for API mode)
- `uvicorn` (for running the API)

---

## 🚀 Setup

From the project folder (`c:\LearningPath-AgenticAI\Grok\SingleAgent`):

```powershell
python -m venv venv
& venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install langgraph langchain_ollama fastapi uvicorn
```

> ✅ Make sure `ollama` is running and the model (e.g., `qwen2.5-coder:7b`) is available locally.

---

## ▶️ Running (CLI mode)

Run the chat loop:

```powershell
python graph_app.py
```

You can also set a custom session/thread ID (to keep history separate):

```powershell
python graph_app.py cli my-session-id
```

Type messages at the prompt. Exit by typing:

- `quit`
- `exit`
- `bye`

---

## ▶️ Running (FastAPI mode)

Start the API server:

```powershell
uvicorn graph_app:fastapi_app --reload
```

Then send chat requests:

```powershell
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"Hi from API","thread_id":"api-session-1"}'
```

Response includes:

- `reply`: latest AI response
- `messages`: full conversation history for that `thread_id`

---

## 🧠 How it works (high level)

- `graph_app.py` builds a `StateGraph` with one node (`chat`) that runs `chatbot()`.
- `SqliteSaver` persists state in `chat_history.db` keyed by `thread_id`.
- Each request (CLI or API) invokes the graph with a new user message and appends the AI reply.

---

## 🔧 Customization

### Change the model

Edit the LLM configuration in `graph_app.py`:

```python
llm = ChatOllama(model="qwen2.5-coder:7b", temperature=0.1)
```

### Change the storage file

Modify the SQLite path in `graph_app.py`:

```python
sqlite_path = "chat_history.db"
```

---

## 📌 Notes

- History is tracked per `thread_id`, so multiple sessions can run concurrently without mixing conversations.
- For production, consider adding:
  - error handling around LLM calls
  - prompt templating and system messages
  - token/context trimming for long conversations
  - configuration via environment variables
