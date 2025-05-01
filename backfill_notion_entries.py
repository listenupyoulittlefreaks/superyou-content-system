# backfill_notion_entries.py

import os
import json
from dotenv import load_dotenv
from content_generation.notion_logger import create_notion_entry

load_dotenv()

# Paths
base_dir = "data/output"
brief_path = os.path.join(base_dir, "brief.json")
post_path = os.path.join(base_dir, "generated_post.txt")
repurpose_path = os.path.join(base_dir, "repurposed_post.txt")
log_path = os.path.join(base_dir, "notion_backfill_log.json")

# Check for existence
if not (os.path.exists(brief_path) and os.path.exists(repurpose_path)):
    print("❌ Required files not found in data/output/.")
    exit()

# Load brief and content
with open(brief_path, "r") as f:
    brief = json.load(f)

with open(repurpose_path, "r") as f:
    repurposed = f.read()

# Use fallback if generated_post is missing
if os.path.exists(post_path):
    with open(post_path, "r") as f:
        post = f.read()
else:
    post = "Post content not found."

# Parse repurposed content
if "Email:" in repurposed:
    social_text = repurposed.split("Email:")[0].strip()
    email_block = repurposed.split("Email:")[1].strip()
    email_subject = "Blog Update"
    email_body = email_block
    if "Subject:" in email_block:
        lines = email_block.splitlines()
        email_subject = lines[0].replace("Subject:", "").strip()
        email_body = "\n".join(lines[1:]).strip()
else:
    social_text = repurposed.strip()
    email_subject = brief.get("title", "New blog post")
    email_body = "Read the full blog post here: [Unavailable]"

# Avoid duplicates by reading log file
if os.path.exists(log_path):
    with open(log_path, "r") as f:
        already_logged = json.load(f)
else:
    already_logged = []

title = brief.get("title")
if title in already_logged:
    print(f"🔁 Already logged '{title}' to Notion. Skipping.")
    exit()

# Send to Notion
print(f"📤 Backfilling: {title}")
try:
    notion_response = create_notion_entry(
        title=title,
        status="Backfilled",
        url="Not published",
        brief=json.dumps(brief, indent=2),
        social_text=social_text,
        email_subject=email_subject,
        email_body=email_body,
        category=brief.get("category", "General")
    )

    if isinstance(notion_response, dict) and "url" in notion_response:
        print(f"✅ Notion entry created: {notion_response['url']}")
    else:
        print("✅ Notion entry created.")

    already_logged.append(title)
    with open(log_path, "w") as f:
        json.dump(already_logged, f, indent=2)

except Exception as e:
    print("❌ Failed to backfill to Notion:", e)