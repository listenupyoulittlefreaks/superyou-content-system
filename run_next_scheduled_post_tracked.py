# run_next_scheduled_post_tracked.py

import os
import json
import sys
from datetime import datetime
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from content_generation.blog_writer import generate_blog_post
from content_generation.post_optimizer import optimize_post
from content_generation.publisher import publish_post
from content_generation.repurposer import repurpose_blog
from content_generation.notion_logger import create_notion_entry

load_dotenv()

rotation_path = os.path.join("resources", "content_rotation.json")
tracker_path = os.path.join("data", "content_rotation_tracker.json")

if not os.path.exists(rotation_path):
    print("❌ content_rotation.json not found.")
    sys.exit()

with open(rotation_path, "r") as f:
    briefs = json.load(f)

if os.path.exists(tracker_path):
    with open(tracker_path, "r") as f:
        used_indexes = json.load(f)
else:
    used_indexes = []

next_index = None
for i in range(len(briefs)):
    if i not in used_indexes:
        next_index = i
        break

if next_index is None:
    print("🔁 All topics used. Resetting rotation.")
    used_indexes = []
    next_index = 0

brief = briefs[next_index]
used_indexes.append(next_index)

os.makedirs("data", exist_ok=True)
with open(tracker_path, "w") as f:
    json.dump(used_indexes, f)

print(f"📅 Selected brief #{next_index + 1}: {brief['title']}")

print("🧠 Generating blog post...")
post = generate_blog_post(brief)

if not post:
    print("❌ Failed to generate blog post.")
    sys.exit()

os.makedirs("data/output", exist_ok=True)
with open("data/output/generated_post.txt", "w") as f:
    f.write(post)

with open("data/output/brief.json", "w") as f:
    json.dump(brief, f, indent=2)

print("✅ Blog post saved.")

print("🔍 Optimizing blog post...")
optimized = optimize_post(post)

if optimized:
    with open("data/output/optimized_post.txt", "w") as f:
        f.write(optimized)
    print("✅ Optimization saved.")
else:
    print("⚠️ Optimization skipped.")

print("📣 Repurposing content...")
repurposed = repurpose_blog(optimized or post)

if repurposed:
    with open("data/output/repurposed_post.txt", "w") as f:
        f.write(repurposed)
    print("✅ Repurposed content saved.")
else:
    print("⚠️ Repurposing failed or skipped.")

print("🚀 Publishing to WordPress...")
post_url = publish_post(
    wp_site=os.getenv("WP_SITE"),
    wp_user=os.getenv("WP_USER"),
    wp_app_password=os.getenv("WP_APP_PASSWORD"),
    title=brief.get("title", "Untitled Blog Post"),
    content=post,
    status="draft"
)

if post_url:
    with open("data/output/automation_status.txt", "w") as f:
        f.write(post_url)

print("DEBUG → post_url:", post_url)
print("DEBUG → repurposed exists:", bool(repurposed))
print("DEBUG → repurposed preview:\n", repurposed[:300])

if repurposed:
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
        email_body = "Read the full blog post here: " + (post_url or "[Unavailable]")

    try:
        print("📤 Sending to Notion...")
        notion_response = create_notion_entry(
            title=brief.get("title", "Untitled Blog Post"),
            status="Draft" if not post_url else "Published",
            url=post_url or "Not published",
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
    except Exception as e:
        print("❌ Failed to log to Notion:", e)
        os.makedirs("logs", exist_ok=True)
        with open("logs/notion_error.log", "a") as f:
            f.write(str(e) + "\n")