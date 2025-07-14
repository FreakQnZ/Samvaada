from typing_extensions import Any
from langchain_core.tools import tool
from db import db

@tool
def sql_db_query(query: str) -> Any:
    """Execute a SQL query on the database and return the result.

    Args:
        query: The SQL query to execute

    Returns:
        The result of the SQL query
    """
    print(f"In sql query with {query}")
    sql_result = db.run(query)
    print(f"SQL Result: {sql_result}")
    return sql_result

@tool
def save_result(result: str) -> str:
    """Save the query result and mark the conversation as completed.

    Args:
        result: The final SQL query result to save

    Returns:
        Updated AgentState with result saved and completed flag set
    """
    print("Saving result...")
    return result

sql_tools = [save_result, sql_db_query]
