import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from dotenv import load_dotenv
from content_generation.publisher import publish_post

# Load environment variables
load_dotenv()

# Check values
wp_site = os.getenv("WP_SITE")
wp_user = os.getenv("WP_USER")
wp_password = os.getenv("WP_APP_PASSWORD")

print("🔍 WP_SITE:", wp_site)
print("🔍 WP_USER:", wp_user)
print("🔍 WP_APP_PASSWORD set:", bool(wp_password))

if not all([wp_site, wp_user, wp_password]):
    raise EnvironmentError("❌ One or more WordPress credentials are missing.")

# Run test publish
post_url = publish_post(
    wp_site=wp_site,
    wp_user=wp_user,
    wp_app_password=wp_password,
    title="Test Post from Script",
    content="This is a test blog post.",
    status="draft"
)

if post_url:
    print(f"✅ Success! Post URL: {post_url}")
else:
    print("❌ Failed to publish post.")