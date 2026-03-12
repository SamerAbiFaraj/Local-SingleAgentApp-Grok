from fastapi import FastAPI
from pydantic import BaseModel
from graph_app import app_graph, shutdown


app = FastAPI(title="LangGraph + Ollama Chat API")

class ChatRequest(BaseModel):
    message: str
    thread_id: str # Allows multi-user/ multi-session (ex: "user-123", "session-xyz")
    

class ChatResponse(BaseModel):
    reply: str
    messages: list[str]
    

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(req: ChatRequest):
    config = {"configurable": {"thread_id": req.thread_id}}
    
    # Invoke LangGraph app with new user message
    result = app_graph.invoke({"messages":[req.message]}, config)
    
    # Last message is AI reply full list is conversation history
    reply = result["messages"][-1]
    return ChatResponse(reply=reply, messages = result["messages"])


@app.on_event("shutdown")
def on_shutdown():
    shutdown()