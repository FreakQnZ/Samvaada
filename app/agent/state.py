from langchain_core.messages import BaseMessage
from typing_extensions import Optional, List, Annotated, TypedDict
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    user_input: str
    clarified_query: str
    schema_context: str
    current_time: str
    messages: Annotated[List[BaseMessage], add_messages]
    message_index: int
    conversational_context: Optional[str]
    completed: bool
