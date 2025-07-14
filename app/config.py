import os
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

MYSQL_USERNAME = os.getenv("MYSQL_USERNAME")
MYSQL_PASSWORD = urllib.parse.quote_plus(os.getenv("MYSQL_PASSWORD", "test"))
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DB = "erp"

DB_URI = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
print("Database URI:", DB_URI)
