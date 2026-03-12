import os
import sys
from typing import TypedDict, Annotated

from fastapi import FastAPI
from pydantic import BaseModel
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_ollama import ChatOllama
import operator

# =========================
# LangGraph Core Definition
# =========================

class State(TypedDict):
    messages: Annotated[list[str], operator.add]

llm = ChatOllama(
    model="qwen2.5-coder:7b",
    temperature=0.1,
)

def chatbot(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response.content]}

# Build graph
graph = StateGraph(State)
graph.add_node("chat", chatbot)
graph.set_entry_point("chat")
graph.add_edge("chat", END)

# SQLite checkpointer (shared by CLI and FastAPI)
sqlite_path = "chat_history.db"
checkpointer_ctx = SqliteSaver.from_conn_string(sqlite_path)
checkpointer = checkpointer_ctx.__enter__()  # enter context once
app_graph = graph.compile(checkpointer=checkpointer)


def shutdown():
    """Gracefully close SQLite."""
    checkpointer_ctx.__exit__(None, None, None)


# =========================
# CLI MODE
# =========================

def run_cli(thread_id: str = "cli-default"):
    config = {"configurable": {"thread_id": thread_id}}

    print("🤖 Continuous Chatbot (type 'quit', 'exit', or 'bye' to stop)")
    print("AI is ready!\n")

    try:
        while True:
            user_input = input("You: ").strip()

            if user_input.lower() in ["quit", "exit", "bye"]:
                print("👋 Goodbye!")
                break

            if not user_input:
                print("Please enter a message.")
                continue

            result = app_graph.invoke({"messages": [user_input]}, config)
            ai_reply = result["messages"][-1]
            print(f"AI: {ai_reply}\n")

        # Optional: show final history
        print("Final conversation history:")
        state = app_graph.get_state(config)
        print(state.values["messages"])
    finally:
        shutdown()


# =========================
# FastAPI MODE
# =========================

fastapi_app = FastAPI(title="LangGraph + Ollama Chat API")

class ChatRequest(BaseModel):
    message: str
    thread_id: str

class ChatResponse(BaseModel):
    reply: str
    messages: list[str]

@fastapi_app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    config = {"configurable": {"thread_id": req.thread_id}}
    result = app_graph.invoke({"messages": [req.message]}, config)
    reply = result["messages"][-1]
    return ChatResponse(reply=reply, messages=result["messages"])

@fastapi_app.on_event("shutdown")
def on_shutdown():
    shutdown()


# =========================
# Entry Point / Mode Switch
# =========================

if __name__ == "__main__":
    """
    Usage options:

    1) CLI mode (default):
       python single_agent.py

    2) CLI mode with custom thread_id:
       python single_agent.py cli my-session-id

    3) FastAPI mode:
       uvicorn single_agent:fastapi_app --reload
    """
    mode = "cli"
    thread_id = "cli-default"

    if len(sys.argv) >= 2:
        mode = sys.argv[1].lower()
    if len(sys.argv) >= 3:
        thread_id = sys.argv[2]

    if mode == "cli":
        run_cli(thread_id=thread_id)
    else:
        print("Unknown mode. Use:\n"
              "  python single_agent.py           # CLI\n"
              "  python single_agent.py cli ID    # CLI with custom thread\n"
              "  uvicorn single_agent:fastapi_app --reload  # FastAPI")
