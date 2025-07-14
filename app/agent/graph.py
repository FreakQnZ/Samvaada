from langgraph.graph import StateGraph, START, END
from agent.state import AgentState
from agent.nodes import (
    setup_node, conversational_qa_node, clarify_query_node, sql_executor_node,
    response_node, route1, route2
)
from agent.tools import sql_tools
from langgraph.prebuilt import ToolNode

def build_agent_app():
    graph = StateGraph(AgentState)
    tool_node = ToolNode(sql_tools)
    graph.add_node("setup", setup_node)
    graph.add_node("qa", conversational_qa_node)
    graph.add_node("clarify_query_node", clarify_query_node)
    graph.add_node("sql_node", sql_executor_node)
    graph.add_node("tools", tool_node)
    graph.add_node("response", response_node)


    graph.add_edge(START, "setup")
    graph.add_edge("setup", "qa")
    graph.add_conditional_edges(
        "qa",
        route1,
        {
            "exit": "response",
            "clarify": "clarify_query_node"
        }
    )
    graph.add_edge("clarify_query_node", "sql_node")
    graph.add_conditional_edges(
        "sql_node",
        route2,
        {
            "exit": "response",
            "tools_use": "tools"
        }
    )
    graph.add_edge("tools", "sql_node")
    graph.add_edge("response", END)

    return graph.compile()
