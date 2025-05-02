import os
from dotenv import load_dotenv
from content_generation.publisher import publish_post
import requests

# Load .env variables
load_dotenv()

# Extract credentials
wp_site = os.getenv("WP_SITE")
wp_user = os.getenv("WP_USER")
wp_app_password = os.getenv("WP_APP_PASSWORD")

# Masked output for safety
print("🔍 WP_SITE:", wp_site or "❌ Missing")
print("🔍 WP_USER:", wp_user or "❌ Missing")
print("🔍 WP_APP_PASSWORD is set:", "✅ Yes" if wp_app_password else "❌ No")

# Debug check for any missing variables
if not all([wp_site, wp_user, wp_app_password]):
    raise EnvironmentError("❌ One or more WordPress credentials are missing from .env")

# Build headers and payload for debug test
url = f"{wp_site}/wp-json/wp/v2/posts"
auth = (wp_user, wp_app_password)
headers = {"Content-Type": "application/json"}
data = {
    "title": "Test from debug script",
    "content": "This is a test blog post from the debug script.",
    "status": "draft"
}

# Run test request
print("📡 Sending request to:", url)
try:
    response = requests.post(url, json=data, headers=headers, auth=auth)
    print("✅ Status Code:", response.status_code)
    print("🧾 Response:", response.text[:1000])  # Print first 1000 chars only
except Exception as e:
    print("❌ Exception occurred:", e)