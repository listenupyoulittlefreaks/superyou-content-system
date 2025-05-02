import os
import requests
from requests.auth import HTTPBasicAuth

WP_SITE = os.getenv("WP_SITE", "https://superyou.org.au")
WP_USER = os.getenv("WP_USER")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

if not WP_USER or not WP_APP_PASSWORD:
    raise ValueError("Environment variables WP_USER and WP_APP_PASSWORD must be set.")

post = {
    "title": "✅ Python Test Post",
    "content": "This was sent using the WordPress REST API!",
    "status": "draft"
}

response = requests.post(
    f"{WP_SITE}/wp-json/wp/v2/posts",
    auth=HTTPBasicAuth(WP_USER, WP_APP_PASSWORD),
    headers={"Content-Type": "application/json"},
    json=post
)

print(f"Status code: {response.status_code}")
print(response.text)   