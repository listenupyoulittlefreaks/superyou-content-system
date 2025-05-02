import os
import streamlit as st
from PIL import Image

st.set_page_config(page_title="Superyou AI Content System Dashboard")

# Clear session if reset param is set
if st.query_params.get("reset"):
    st.session_state.clear()
    
import os
from openai import OpenAI
import streamlit as st
from PIL import Image

from content_generation.blog_writer import generate_blog_post
from content_generation.post_optimizer import optimize_post
from content_generation.repurposer import repurpose_blog
from content_generation.publisher import publish_post

st.markdown(
    "<h1 style='color: #37215A;'>Superyou AI Content System Dashboard</h1>",
    unsafe_allow_html=True,
)

prompt_input = st.text_area("✍️ Drop in a custom blog prompt (optional)", "")

if st.button("Generate from Prompt"):
    if prompt_input.strip():
        st.session_state["custom_prompt"] = prompt_input.strip()

brief = {
    "title": "Test Post",
    "prompt": st.session_state.get("custom_prompt") or "Write a blog post about how play therapy supports emotional regulation in autistic children.",
    "category": "NDIS"
}

# Step 1: Generate blog
st.markdown("### 🧠 Generating blog...")
blog_post = generate_blog_post(brief)
if blog_post:
    st.success("Blog generated!")
    st.text_area("Generated Blog Post", blog_post, height=300)

# Step 2: Optimize
st.markdown("### 🔍 Optimizing...")
optimized_post = optimize_post(blog_post)
if optimized_post:
    st.success("Optimized!")
    st.text_area("Optimized Post", optimized_post, height=300)

# Step 3: Repurpose
st.markdown("### 📣 Repurposing...")
repurposed = repurpose_blog(optimized_post or blog_post)
if repurposed:
    st.success("Repurposed!")
    st.text_area("Repurposed Content", repurposed, height=250)

# Step 4: Extract email subject line
lines = repurposed.split("\n") if repurposed else []
subject_line = ""
preview = ""

for line in lines:
    if line and "Subject:" in line:
        subject_line = (line or "").split("Subject:")[-1].strip()
    elif line and "EMAIL:" in line:
        preview = (line or "").strip()

# Display
st.markdown(f"**📬 Email Subject:** {subject_line}")
st.markdown(f"**📩 Email Preview:** {preview}")

# Step 5: Publish
st.markdown("### 🚀 Publish to WordPress")
if st.button("Publish Now"):
    post_url = publish_post(
        wp_site=os.getenv("WP_SITE"),
        wp_user=os.getenv("WP_USER"),
        wp_app_password=os.getenv("WP_APP_PASSWORD"),
        title=brief["title"],
        content=optimized_post or blog_post,
        status="draft"
    )
    if post_url:
        st.success(f"Published: {post_url}")
    else:
        st.error("❌ Failed to publish.")