from fastapi import APIRouter
from schema import AskRequest
from langchain_core.messages import HumanMessage, AIMessage
from agent.graph import build_agent_app

router = APIRouter()
compiled_app = build_agent_app()

@router.post("/ask")
async def ask(request: AskRequest):
    base_messages = [HumanMessage(content=m) if i % 2 != 0 else AIMessage(content=m) for i, m in enumerate(request.messages)]
    inputs = {
        "user_input": request.user_input,
        "messages": base_messages
    }
    print(f"Input: {inputs}")
    result = compiled_app.invoke(inputs)
    reply = result["messages"][-1].content
    return {
        "response": reply,
        "messages": [m.content for m in result["messages"]]
    }
