# content_generation/notion_logger.py

import os
import requests
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def create_notion_entry(title, status, url, brief, social_text, email_subject, email_body, category=None):
    created_time = datetime.now().isoformat()

    data = {
        "parent": { "database_id": NOTION_DATABASE_ID },
        "properties": {
            "Title": {
                "title": [{ "text": { "content": title } }]
            },
            "Status": {
                "select": { "name": status }
            },
            "Published URL": {
                "url": url
            },
            "Generated At": {
                "date": { "start": created_time }
            },
            "Topic Category": {
                "select": { "name": category or "General" }
            },
            "Repurposed Email": {
                "rich_text": [{
                    "text": {
                        "content": f"Subject: {email_subject}\n\n{email_body}"
                    }
                }]
            },
            "Repurposed Social": {
                "rich_text": [{
                    "text": {
                        "content": social_text
                    }
                }]
            },
            "Brief": {
                "rich_text": [{
                    "text": {
                        "content": brief
                    }
                }]
            }
        }
    }

    res = requests.post("https://api.notion.com/v1/pages", headers=NOTION_HEADERS, json=data)

    if res.status_code == 200:
        print("✅ Notion entry created.")
    else:
        print(f"❌ Failed to create Notion entry: {res.status_code}")
        print(res.text)