from datetime import datetime
from langchain_core.messages import HumanMessage
from agent.state import AgentState
from db import db
from context import get_schema_context
from agent.tools import sql_tools
from langchain_groq import ChatGroq

llm = ChatGroq(model="gemma2-9b-it")

def setup_node(state: AgentState) -> AgentState:
    """
    Setup node for initializing the agent's state.

    This function enriches the initial state with:
    - The current UTC time (used for resolving relative date queries like "today")
    - Schema context for the 'sales_order' and 'customer' tables
    - Sample rows from both tables to assist in generating accurate SQL
    - An attempt counter initialized to 0
    - A message history initialized with the user's input as the first HumanMessage
    """
    state["current_time"] = datetime.utcnow().isoformat()
    state["clarified_query"] = ""
    state["schema_context"] = get_schema_context(db)
    state["messages"].append(HumanMessage(content=state["user_input"]))
    state["conversational_context"] = ""
    state["completed"] = False
    state["message_index"] = len(state["messages"])
    # state["message_index"] = 0
    return state

def conversational_qa_node(state: AgentState) -> AgentState:
    """
    Checks whether the current question can be answered directly from prior conversation.
    Otherwise, leaves state untouched so it can proceed to clarification.
    """
    history_text = "\n".join([f"{msg.type.upper()}: {msg.content}" for msg in state["messages"]])
    # prompt = (
    #     "You are a conversational assistant called Samvada sitting above an SQL-based QA agent. "
    #     "Your role is to assess if user questions can be answered using **only**:\n"
    #     "- The provided conversation history\n"
    #     "- General common knowledge (e.g., basic math, greetings)\n"
    #     "- **Without** relying on new database queries or external information\n\n"
    #     "If the question requires a database query, respond with exactly 'CANNOT_ANSWER'\n"

    #     "You **must not make assumptions or invent facts**.\n"
    #     "You **must not** use any information not present in the conversation history or common knowledge.\n\n"

    #     "Here is the conversation history:\n"
    #     f"{history_text}\n\n"

    #     "Now, determine if the latest human message is a general or conversational query (e.g., 'Hi', 'Thanks') , if it is a general query like that you will also greet back saying 'Hello I am a database assistant'"
    #     "or if it can be answered based on prior conversation context.\n\n"

    #     "If you can answer it appropriately within those constraints, provide the answer directly.\n"
    #     "If you cannot answer it within those limits, respond with exactly:\n"
    #     "CANNOT_ANSWER"
    # )
    prompt = (
        "You are a conversational assistant called Samvada sitting above an SQL-based QA agent.\n"
        "Your role is to classify the latest user message into one of the following:\n"
        "1. If the message is a general conversational input (e.g., 'Hi', 'Thanks', 'Bye'), respond with exactly: CONVERSATIONAL\n"
        "2. If the message requires a database query to be answered, respond with exactly: CANNOT_ANSWER\n"
        "3. If you can answer it based only on prior conversation or common knowledge, answer normally.\n\n"
        "Rules:\n"
        "- Do not assume anything outside the history provided.\n"
        "- Do not invent database-related answers.\n\n"
        "- Answer should not be I'm sorry I dont have access, or I do not know, if that is the case then you need it is likely that the answer is available in the database so you should respond with: CANNOT_ANSWER"
        "Here is the conversation history:\n"
        f"{history_text}\n\n"
        "Now determine what to respond."
    )

    # response = llm.invoke(prompt)
    # if "CANNOT_ANSWER" not in str(response.content).upper():
    #     state["messages"] = [response]
    #     state["completed"] = True
    # return state
    #
    response = llm.invoke(prompt)
    content = str(response.content).strip().upper()

    if "CANNOT_ANSWER" in content:
        return state  # Continue to clarification
    elif "CONVERSATIONAL" in content:
        state["messages"] = [response]  # Will respond directly
        state["completed"] = True
        return state
    else:
        # It's a valid answer from context
        state["messages"] = [response]
        state["completed"] = True
        return state

def route1(state: AgentState) -> str:
    """
    Route to the next node in the graph.
    """
    if state["completed"]:
        return "exit"
    else:
        return "clarify"

def update_conversational_context(state: AgentState, history: str) -> AgentState:
    """
    Uses the LLM to extract only the parts of the conversation that are relevant
    to understanding the current question.
    """
    prompt = (
        "Given the following conversation history, extract only the minimal relevant context "
        "needed to understand and answer the user's most recent question. which is the last human question\n\n"
        f"{history}\n\n"
        "You will only respond with the relevant context and nothing else."
    )
    response = llm.invoke(prompt)
    state["conversational_context"] = str(response.content)
    return state

def update_clarified_query(state: AgentState, history: str) -> AgentState:
    """
    Reformulates the user's question into a clear, unambiguous standalone query.
    """
    prompt = (
        "Rewrite the following user question to be fully unambiguous and standalone. "
        "You have been provided conversation history, you will use this information to clarify the question."
        "Avoid vague phrases like 'today', 'this month', etc. unless absolutely necessary.\n\n"
        f"History: {history}\n\n"
        f"Current time: {state['current_time']}, only include time in query if required (example: user asks how many sales is done today)\n\n"
        f"Original Question: {state['user_input']}\n\n"
        f"The original question is also the last Human Message in the history provided. You have to make it a standalone query."
        "You will only respond with the clarified query and nothing else."
    )
    response = llm.invoke(prompt)
    state["clarified_query"] = str(response.content)
    return state

def clarify_query_node(state: AgentState) -> AgentState:
    """
    Clarifies the user query and extracts conversational context using helper tools.
    """
    print("Entered clarify_query_node")
    history_text = "\n".join(
        [f"{msg.type.upper()}: {msg.content}" for msg in state["messages"]]
    )
    print("Updating conversational context")
    state = update_conversational_context(state, history_text)
    print(f"Conversational context: {state['conversational_context']}")
    print("Updating clarified query")
    state = update_clarified_query(state, history_text)
    print(f"Clarified Query: {state['clarified_query']}")
    return state

def sql_executor_node(state: AgentState) -> AgentState:
    """
    Forms Appropriate SQL Query from unambiguous user query and executes it using the provided tools.
    """
    messages = state["messages"][state["message_index"]:]

    llm_tool = llm.bind_tools(sql_tools)
    # prompt = (
    #     f"Form an appropriate SQL query from the following unambiguous user query: {state['clarified_query']}\n\n"
    #     f"You have also been provided some context: {state['conversational_context']}\n\n"
    #     "You will form the query using the below provided details of the MySQL Database.\n"
    #     f"Schema and rows: {state['schema_context']}\n\n"
    #     "Once query is formed run it using sql_db_query tool.\n"
    #     "Once you receive answer run the save_result tool where you'll pass the answer."
    # )
    prompt = (
        f"You are an expert SQL generator.\n\n"
        f"Your job is to write a SQL query from the following clarified user query:\n"
        f"---\n{state['clarified_query']}\n---\n\n"

        f"You may also use the conversational context:\n"
        f"---\n{state['conversational_context']}\n---\n\n"

        f"Use the following schema and sample rows to generate valid SQL:\n"
        f"---\n{state['schema_context']}\n---\n\n"
        f"The physical entities like open or closed are stored as numbers in the database. For example, 'open' is represented as 1 and 'closed' is represented as 7.\n"
        f"Here are the mappings for enumerated columns in the database:\n"
        f"- CATEGORY_ID:\n"
        f"    1 = 'Part'\n"
        f"    2 = 'BOM' (or 'bom')\n"
        f"- SO_TYPE_ID:\n"
        f"    1 = 'confirm'\n"
        f"    2 = 'trend'\n"
        f"    3 = 'forecast'\n"
        f"- STATUS_ID:\n"
        f"    1 = 'open'\n"
        f"    5 = 'on hold'\n"
        f"    6 = 'cancelled'\n"
        f"    7 = 'close'\n"
        f"    8 = 'on hold auto close'\n"
        f"    9 = 'auto close'\n"
        f"- STAGE_STATUS_ID:\n"
        f"    1 = 'open'\n"
        f"    2 = 'assigned'\n"
        f"    3 = 'delivered'\n"
        f"    4 = 'partial'\n\n"
        f" Make sure to use the correct mappings for enumerated columns in the database.\n"
        f"IMPORTANT:\n"
        f"- If the user does **not** specify otherwise, assume:\n"
        f"    - Only orders where `STAGE_STATUS_ID = 3` (delivered)\n"
        f"    - Only orders where `SO_TYPE_ID = 1` (confirmed)\n"
        f"- Apply these filters unless the user explicitly overrides them.\n\n"

        f"Now, generate an appropriate SQL query based on the above.\n"
        f"Once query is ready, call `sql_db_query` tool to run it.\n"
        # f"Then, pass the result to `save_result` tool to finalize the response.\n"
        f"Once you receive answer run the save_result tool where you'll pass the answer."
    )
    # print(f"Messages: {messages}")
    # pretty_print_messages(messages)
    response = llm_tool.invoke([prompt]+messages)
    # print(f"Tool used: {response.tool_calls[0]}")
    # print(f"response {response.content}")
    state["messages"] = [response]
    return state

def route2(state: AgentState) -> str:
    """
    Route to the next node in the graph based on SQL check
    """
    messages = state["messages"]
    last_message = messages[-1]
    if not last_message.tool_calls:
        return "exit"
    else:
        return "tools_use"

def response_node(state: AgentState) -> AgentState:
    # "The answer should be of the form: <Sure! Based on the data, {your answer in a conversational manner here}>"
    messages = state["messages"][state["message_index"]:]
    prompt = (
        "You are a answer formulator, your name is 'Samvada', you are given the original query, and the working of an Agentic AI which has found the answer."
        "You will respond to the original question in a nice conversation manner using the answer in the working of the Agentic AI."

        "If anyone asks who you are you shall say I am 'Samvada a database assistant'"
        f"Orginal User question: {state['user_input']}"
        f"Agentic AI Working: {messages}"
    )
    response = llm.invoke(prompt)
    state["messages"] = [response]
    print(response.content)
    return state
