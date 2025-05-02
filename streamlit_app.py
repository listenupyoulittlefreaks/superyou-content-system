import os
import streamlit as st
from PIL import Image
from openai import OpenAI

from content_generation.blog_writer import generate_blog_post
from content_generation.post_optimizer import optimize_post
from content_generation.repurposer import repurpose_blog
from content_generation.publisher import publish_post

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Optional: clear session on ?reset=true
if st.experimental_get_query_params().get("reset"):
    st.session_state.clear()

st.set_page_config(page_title="Superyou AI Content System Dashboard")
st.markdown("<h1 style='color: #37215A;'>Superyou AI Content System Dashboard</h1>", unsafe_allow_html=True)

# INPUT: Custom prompt
prompt_input = st.text_area("✍️ Drop in a custom blog prompt (optional)", "")

if st.button("Generate from Prompt"):
    if prompt_input.strip():
        st.session_state["custom_prompt"] = prompt_input.strip()

# PREP BRIEF
brief = {
    "title": "Test Post",
    "prompt": st.session_state.get("custom_prompt") or "Write a blog post about how play therapy supports emotional regulation in autistic children.",
    "category": "NDIS"
}

# MODULE 1: Blog Generation
st.markdown("### 🧠 Generating blog...")
blog_post = generate_blog_post(brief)
if blog_post:
    st.success("✅ Blog generated!")
    st.text_area("📝 Generated Blog", blog_post, height=300)

# MODULE 2: Optimization
st.markdown("### 🔍 Optimizing post...")
optimized_post = optimize_post(blog_post)
if optimized_post:
    st.success("✅ Post optimized!")
    st.text_area("📈 Optimized Version", optimized_post, height=300)

# MODULE 3: Repurposing
st.markdown("### 📣 Repurposing...")
repurposed = repurpose_blog(optimized_post or blog_post)
if repurposed:
    st.success("✅ Repurposed successfully!")
    st.text_area("📢 Repurposed Content", repurposed, height=250)

# Extract email parts
lines = repurposed.split("\n") if repurposed else []
subject_line = ""
preview = ""
for line in lines:
    if line and "Subject:" in line:
        subject_line = (line or "").split("Subject:")[-1].strip()
    elif line and "EMAIL:" in line:
        preview = (line or "").strip()

st.markdown(f"**📬 Email Subject:** {subject_line}")
st.markdown(f"**📩 Email Preview:** {preview}")

# MODULE 4: Publishing
st.markdown("### 🚀 Publish to WordPress")
if st.button("📤 Publish Now"):
    post_url = publish_post(
        wp_site=os.getenv("WP_SITE"),
        wp_user=os.getenv("WP_USER"),
        wp_app_password=os.getenv("WP_APP_PASSWORD"),
        title=brief["title"],
        content=optimized_post or blog_post,
        status="draft"
    )
    if post_url:
        st.success(f"✅ Post published: {post_url}")
        st.session_state["last_post_url"] = post_url
    else:
        st.error("❌ Failed to publish.")

# MODULE 5: Publishing Status
st.markdown("### 📊 Publishing Status")
if "last_post_url" in st.session_state:
    st.markdown(f"🔗 Most recent post: [{st.session_state['last_post_url']}]({st.session_state['last_post_url']})")
else:
    st.info("No recent post published.")

# MODULE 6: Analytics Preview (placeholder)
st.markdown("### 📈 Analytics Preview (Coming Soon)")
st.write("This module will pull metrics from Google Analytics and Search Console.")