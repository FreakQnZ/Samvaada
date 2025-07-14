from langchain_community.utilities import SQLDatabase
from dotenv import load_dotenv
import os
import urllib.parse

print("Connected to DB in context.py")
def get_schema_context(db) -> str:
    """Returns schema for sales_order and customer tables."""
    table_info = db.get_table_info(["sales_order", "customer"])
    # print(table_info)
    return table_info


if __name__ == "__main__":
    load_dotenv()

    user = os.getenv('MYSQL_USERNAME')
    password = urllib.parse.quote_plus(os.getenv('MYSQL_PASSWORD') or "test")
    host = "localhost"
    port = 3306
    database = "erp"

    DB_URI = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    print(f"Connecting to DB with uri {DB_URI}")
    db = SQLDatabase.from_uri(DB_URI)
    print("Connection established")
    print(get_schema_context(db))
