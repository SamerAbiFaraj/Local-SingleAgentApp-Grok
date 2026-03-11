# SingleAgent Chatbot# SingleAgent Chatbot






























































































If you want, I can also add a `requirements.txt` and a `python -m venv` setup script to make bootstrapping smoother.---- `chat_history.db` – generated at runtime (stores conversation state)- `SingleAgent.py` – main script## 🗂️ Files```with SqliteSaver.from_conn_string("chat_history.db") as checkpointer:```pythonUpdate the filename in:### Change history storage file```llm = ChatOllama(model="qwen2.5-coder:7b", temperature=0.1)```pythonIn `SingleAgent.py`, update the `ChatOllama` instantiation:### Change the LLM model## 🔧 Customization  4. Saves state automatically via the graph's checkpoint  3. Prints the latest LLM response  2. Sends messages to the LLM via `ChatOllama.invoke`  1. Reads user input- Each loop iteration:- `SqliteSaver` wraps a SQLite file (`chat_history.db`) to persist state.- `StateGraph` defines a simple graph with one node (`chat`) that calls `chatbot()`.## 🧠 How it works (high level)- `bye`- `exit`- `quit`To exit, type:Type a message and press Enter. The bot will respond and store the history in `chat_history.db`.```You: ```You will see a prompt:```python SingleAgent.py```powershellFrom the project folder, run:## ▶️ Run> ⚠️ If you are using a private or custom Ollama model, ensure your Ollama instance is running and accessible.```pip install langgraph langchain_ollama```powershell2) Install the required packages:```& venv\Scripts\Activate.ps1python -m venv venv```powershell1) Create and activate a virtual environment (recommended):## 🚀 Install & SetupIt also assumes your Ollama model is available and that the `ChatOllama` constructor works with your setup.- `langchain_ollama`- `langgraph`This project expects a Python environment with these packages installed:## 📦 Requirements- Runs in the terminal, accepting user input until you type `quit`, `exit`, or `bye`- Persists conversation history via `SqliteSaver` so the bot can continue across runs- Uses **ChatOllama** (from `langchain_ollama`) to call a local or remote Ollama model- Uses **langgraph** to model a stateful chat graph## ✅ What this doesA simple continuous chatbot built using **langgraph** and **langchain_ollama**. It keeps conversation history in a local SQLite database (`chat_history.db`) and allows you to interact with an LLM in a loop.
This project is a minimal example of a **continuous chatbot** using `langgraph` and `langchain_ollama`.

It maintains conversation history in an SQLite database and lets you have an interactive chat loop without rebuilding state every prompt.

---

## 🧩 What this code does

- Defines a simple `State` schema for storing chat messages.
- Uses `langgraph` to build a state graph with a single node (`chat`) that calls an LLM.
- Wraps state persistence with `SqliteSaver` (stores history in `chat_history.db`).
- Starts an interactive CLI loop where you can type messages and see the AI reply.

---

## ✅ Requirements

### Python
- Python 3.10+ (recommended)

### Dependencies
The code depends on the following packages:

- `langgraph`
- `langchain_ollama`

It also uses the `qwen2.5-coder:7b` model via **Ollama**, so you need:

- `ollama` installed and configured on your system
- The `qwen2.5-coder:7b` (or another Ollama model) available locally

> 💡 If you want to use a different model, update the `model=` argument in `SingleAgent.py`.

---

## 🚀 Installation

From the project folder (`c:\LearningPath-AgenticAI\Grok\SingleAgent`):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install langgraph langchain_ollama
```

> ⚠️ Make sure `ollama` is installed and running (or otherwise accessible) on your system.

---

## ▶️ Running the chatbot

From the project folder while the venv is active:

```powershell
python SingleAgent.py
```

Then type messages at the prompt. To exit, type:

- `quit`
- `exit`
- `bye`

---

## 🗄️ Conversation history

- Conversation history is persisted to `chat_history.db` in the project folder.
- Each run will load previous history (via `SqliteSaver`) and append new messages.

---

## 🔧 Customization

- Change the model by editing the `llm = ChatOllama(...)` line.
- Modify the system prompt / message formatting by adjusting how `state["messages"]` is constructed.

---

## 📌 Notes

- This is a minimal demo and does not handle advanced features like multi-turn context trimming, prompting guidelines, or error handling for failed model calls.
- For production use, consider adding:
  - error handling around the LLM call
  - prompt templates
  - token / context management
  - configuration via environment variables
