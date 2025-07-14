from langchain_community.utilities import SQLDatabase
from config import DB_URI

db = SQLDatabase.from_uri(DB_URI)
