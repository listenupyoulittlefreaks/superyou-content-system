# run_next_scheduled_post.py

import os
import json
import sys
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Extend system path to access modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from content_generation.blog_writer import generate_blog_post
from content_generation.post_optimizer import optimize_post
from content_generation.publisher import publish_post

# Load environment variables
load_dotenv()

# Load the content rotation plan
rotation_path = os.path.join("resources", "content_rotation.json")
if not os.path.exists(rotation_path):
    print("❌ content_rotation.json not found in resources/")
    sys.exit()

with open(rotation_path, "r") as f:
    briefs = json.load(f)

# Use today's date to find the index in the rotation (starting from 1 May 2025)
start_date = datetime(2025, 5, 1)
today = datetime.today()
index = (today - start_date).days // 7 % len(briefs)
brief = briefs[index]

print(f"📅 Selected brief #{index + 1}: {brief['title']}")

# Create output directory
os.makedirs("data/output", exist_ok=True)

# Step 1: Generate the blog post
print("🧠 Generating blog post...")
post = generate_blog_post(brief)

if not post:
    print("❌ Failed to generate blog post.")
    sys.exit()

with open("data/output/generated_post.txt", "w") as f:
    f.write(post)

with open("data/output/brief.json", "w") as f:
    json.dump(brief, f, indent=2)

print("✅ Blog post saved.")

# Step 2: Optimize the post
print("🔍 Optimizing blog post...")
optimized = optimize_post(post)

if optimized:
    with open("data/output/optimized_post.txt", "w") as f:
        f.write(optimized)
    print("✅ Optimization saved.")
else:
    print("⚠️ Skipped optimization due to error.")

# Step 3: Publish the post
print("🚀 Publishing to WordPress...")
publish_post(
    wp_site=os.getenv("WP_SITE"),
    wp_user=os.getenv("WP_USER"),
    wp_app_password=os.getenv("WP_APP_PASSWORD"),
    title=brief.get("title", "Untitled Blog Post"),
    content=post,
    status="draft"
)