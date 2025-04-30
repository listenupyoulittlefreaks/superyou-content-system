# content_generation/publisher.py

import requests
import os
import base64
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
wp_site = os.getenv("WP_SITE")
wp_user = os.getenv("WP_USER")
wp_app_password = os.getenv("WP_APP_PASSWORD")

def publish_post(wp_site, wp_user, wp_app_password, title, content, status='draft'):
    credentials = f"{wp_user}:{wp_app_password}"
    token = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    headers = {
        'Authorization': f'Basic {token}',
        'Content-Type': 'application/json',
        'User-Agent': 'SmartContentSystem/1.0'
    }

    post = {
        'title': title,
        'content': content,
        'status': status
    }

    try:
        response = requests.post(
            f"{wp_site}/wp-json/wp/v2/posts",
            headers=headers,
            json=post
        )

        if response.status_code == 201:
            print("✅ Post published successfully!")
            print("Post URL:", response.json().get("link"))
        else:
            print(f"❌ Failed to publish. Status code: {response.status_code}")
            print("Response:", response.content)

    except Exception as e:
        print(f"❌ Error publishing post: {e}")