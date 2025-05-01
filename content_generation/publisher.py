# content_generation/publisher.py

import requests
import base64

def publish_post(wp_site, wp_user, wp_app_password, title, content, status="draft"):
    url = f"{wp_site}/wp-json/wp/v2/posts"
    credentials = f"{wp_user}:{wp_app_password}"
    token = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json"
    }

    data = {
        "title": title,
        "content": content,
        "status": status
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code in [200, 201]:
        post = response.json()
        print("✅ Post published successfully!")
        print("Post URL:", post.get("link"))
        return post.get("link")
    else:
        print(f"❌ Failed to publish. Status code: {response.status_code}")
        print("Response:", response.content)
        return None