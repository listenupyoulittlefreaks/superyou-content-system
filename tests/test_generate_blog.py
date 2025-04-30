# tests/test_generate_blog.py

import sys
import os
import json
from dotenv import load_dotenv

# Access the generate_blog_post function
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from content_generation.blog_writer import generate_blog_post

load_dotenv()

# Define the brief
brief = {
    "title": "How AAC Supports Communication for Non-Speaking Children",
    "keywords": ["AAC", "speech therapy", "NDIS communication tools"],
    "headings": ["What is AAC?", "Different Types of AAC", "Benefits for Kids"],
    "goal": "Educate parents and support workers about how AAC tools can empower communication."
}

# Generate blog post
post = generate_blog_post(brief)

# Save generated post
if post:
    os.makedirs("data/output", exist_ok=True)
    with open("data/output/generated_post.txt", "w") as f:
        f.write(post)
    with open("data/output/brief.json", "w") as f:
        json.dump(brief, f, indent=2)
    print("✅ Blog post and brief saved successfully.")
else:
    print("❌ Failed to generate blog post.")