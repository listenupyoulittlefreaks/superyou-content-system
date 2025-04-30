# tests/test_publish.py

import sys
import os
import json

# Add root to path so it can find content_generation
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from content_generation.publisher import publish_post

# Load blog post content
content_path = os.path.join("data", "output", "generated_post.txt")
brief_path = os.path.join("data", "output", "brief.json")

if not os.path.exists(content_path) or not os.path.exists(brief_path):
    print("❌ Missing content or brief. Please generate the post first.")
    exit()

with open(content_path, "r") as f:
    content = f.read()

with open(brief_path, "r") as f:
    brief = json.load(f)

title = brief.get("title", "Untitled Blog Post")

# Publish to WordPress
publish_post(
    wp_site=os.getenv("WP_SITE"),
    wp_user=os.getenv("WP_USER"),
    wp_app_password=os.getenv("WP_APP_PASSWORD"),
    title=title,
    content=content,
    status="draft"
)