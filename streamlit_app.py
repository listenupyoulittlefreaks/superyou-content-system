# streamlit_app.py

import streamlit as st
import os
import json
from PIL import Image
from content_generation.blog_writer import generate_blog_post
from content_generation.post_optimizer import optimize_post
from content_generation.repurposer import repurpose_blog
from content_generation.publisher import publish_post
from content_generation.image_creator import generate_images
from content_generation.notion_logger import create_notion_entry
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="Superyou AI Dashboard", layout="wide")

# Load logo and display header
logo_path = "SUPERYOU Brand PURPLE_smallv4.png"
if os.path.exists(logo_path):
    col_logo, col_title = st.columns([1, 8])
    with col_logo:
        st.image(Image.open(logo_path), width=50)
    with col_title:
        st.markdown("<h1 style='color:#37215A;'>Superyou AI Content System Dashboard</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='color:#37215A;'>Superyou AI Content System Dashboard</h1>", unsafe_allow_html=True)

output_dir = "data/output"
image_dir = "data/images"
os.makedirs(output_dir, exist_ok=True)
os.makedirs(image_dir, exist_ok=True)

# 🔠 Blog Post Prompt Input
st.markdown("### 💬 <span style='color:#FFDB1C;'>Generate a Blog from Prompt</span>", unsafe_allow_html=True)
user_prompt = st.text_input("Enter a custom blog post prompt:")
run_generate = st.button("🚀 Generate & Publish")

if run_generate and user_prompt:
    st.info("Generating full pipeline from prompt...")
    brief = {"title": user_prompt, "category": "Manual Entry"}
    
    generated = generate_blog_post(brief)
    optimized = optimize_post(generated)
    repurposed = repurpose_blog(optimized or generated)
    generate_images(title=brief["title"], brief=brief)

    post_url = publish_post(
        wp_site=os.getenv("WP_SITE"),
        wp_user=os.getenv("WP_USER"),
        wp_app_password=os.getenv("WP_APP_PASSWORD"),
        title=brief["title"],
        content=optimized or generated,
        status="draft"
    )

    with open(os.path.join(output_dir, "generated_post.txt"), "w") as f:
        f.write(generated or "")
    with open(os.path.join(output_dir, "optimized_post.txt"), "w") as f:
        f.write(optimized or "")
    with open(os.path.join(output_dir, "repurposed_post.txt"), "w") as f:
        f.write(repurposed or "")
    with open(os.path.join(output_dir, "brief.json"), "w") as f:
        json.dump(brief, f, indent=2)
    with open(os.path.join(output_dir, "automation_status.txt"), "w") as f:
        f.write(post_url or "")

    # Parse email and social sections
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
        email_subject = brief["title"]
        email_body = f"Read the full blog post here: {post_url or 'Unavailable'}"

    create_notion_entry(
        title=brief["title"],
        status="Published" if post_url else "Draft",
        url=post_url or "Not published",
        brief=json.dumps(brief, indent=2),
        social_text=social_text,
        email_subject=email_subject,
        email_body=email_body,
        category=brief.get("category", "Manual")
    )

    st.success("✅ Blog generated, published to WordPress, and logged to Notion!")

# Display generated content
col1, col2 = st.columns(2)

with col1:
    st.markdown("### ✍️ <span style='color:#FFDB1C;'>Generated Blog Post</span>", unsafe_allow_html=True)
    gen_path = os.path.join(output_dir, "generated_post.txt")
    if os.path.exists(gen_path):
        with open(gen_path) as f:
            st.text_area("Generated Post", f.read(), height=300)
    else:
        st.warning("generated_post.txt not found.")

with col2:
    st.markdown("### 📣 <span style='color:#FFDB1C;'>Repurposed Content</span>", unsafe_allow_html=True)
    rep_path = os.path.join(output_dir, "repurposed_post.txt")
    if os.path.exists(rep_path):
        with open(rep_path) as f:
            st.text_area("Social + Email", f.read(), height=300)
    else:
        st.warning("repurposed_post.txt not found.")

# Full width brief + images
st.markdown("---")
brief_path = os.path.join(output_dir, "brief.json")
st.markdown("### 📄 <span style='color:#FFDB1C;'>Blog Brief</span>", unsafe_allow_html=True)
if os.path.exists(brief_path):
    with open(brief_path) as f:
        st.json(json.load(f))
else:
    st.warning("brief.json not found.")

# Display generated images if available
st.markdown("### 🖼️ <span style='color:#FFDB1C;'>Generated Images</span>", unsafe_allow_html=True)
image_files = [f for f in os.listdir(image_dir) if f.lower().endswith(".png")]
image_files.sort()
if image_files:
    cols = st.columns(len(image_files))
    for col, img_file in zip(cols, image_files[-2:]):
        col.image(os.path.join(image_dir, img_file), caption=img_file)
else:
    st.info("No generated images found.")

# Show WordPress or Notion sync status
status_path = os.path.join(output_dir, "automation_status.txt")
if os.path.exists(status_path):
    with open(status_path) as f:
        st.success(f"✅ Last Published URL: {f.read().strip()}")
else:
    st.info("ℹ️ No publish status found.")