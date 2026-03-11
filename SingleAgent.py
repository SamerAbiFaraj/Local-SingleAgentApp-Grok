from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
from langgraph.checkpoint.sqlite import SqliteSaver
from langchain_ollama import ChatOllama
import operator


class State(TypedDict): 
    messages: Annotated[list[str], operator.add]


llm = ChatOllama(
    model="qwen2.5-coder:7b",
    temperature=0.1
)


def chatbot(state: State):
    response = llm.invoke(state["messages"])
    return {"messages": [response.content]}


graph = StateGraph(State)
graph.add_node("chat", chatbot)
graph.set_entry_point("chat")
graph.add_edge("chat", END)

config = {"configurable": {"thread_id": "abc123"}}

print("🤖 Continuous Chatbot (type 'quit', 'exit', or 'bye' to stop)")
print("AI is ready!\n")

# IMPORTANT: use SqliteSaver as a context manager
with SqliteSaver.from_conn_string("chat_history.db") as checkpointer:
    app = graph.compile(checkpointer=checkpointer)

    while True:
        user_input = input("You: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'bye']:
            print("👋 Goodbye!")
            break
        
        if not user_input:
            print("Please enter a message.")
            continue
        
        # Send user input - automatically loads history + adds new message
        result = app.invoke({"messages": [user_input]}, config)
        
        # Print latest AI response
        ai_reply = result["messages"][-1]
        print(f"AI: {ai_reply}\n")

    # Optional: Show final conversation history
    print("Final conversation history:")
    state = app.get_state(config)
    print(state.values["messages"])
