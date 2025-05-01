import os
from dotenv import load_dotenv

load_dotenv()

print("Token:", os.getenv("NOTION_TOKEN"))
print("Database ID:", os.getenv("NOTION_DATABASE_ID"))