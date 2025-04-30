# run_full_pipeline.py

import os
import sys
import json
from dotenv import load_dotenv

# Extend system path to use content_generation modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from content_generation.blog_writer import generate_blog_post
from content_generation.post_optimizer import optimize_post
from content_generation.publisher import publish_post

# Load environment variables
load_dotenv()

# Define a rotating brief (this can be expanded or randomized later)
brief = {
    "title": "Supporting Emotional Regulation in Autistic Children",
    "keywords": ["emotional regulation", "autism", "parenting strategies"],
    "headings": ["What is Emotional Regulation?", "Why It's Difficult for Some Kids", "How to Support It"],
    "goal": "Help parents understand and support emotional regulation in autistic children."
}

# Create output directory
os.makedirs("data/output", exist_ok=True)

# Step 1: Generate the blog post
print("🧠 Generating blog post...")
post = generate_blog_post(brief)

if not post:
    print("❌ Failed at blog generation step.")
    sys.exit()

with open("data/output/generated_post.txt", "w") as f:
    f.write(post)

with open("data/output/brief.json", "w") as f:
    json.dump(brief, f, indent=2)

print("✅ Blog post saved to data/output/generated_post.txt")

# Step 2: Optimize the post
print("🔍 Optimizing blog post...")
optimized = optimize_post(post)

if optimized:
    with open("data/output/optimized_post.txt", "w") as f:
        f.write(optimized)
    print("✅ Optimization saved to data/output/optimized_post.txt")
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
    status='draft'
)