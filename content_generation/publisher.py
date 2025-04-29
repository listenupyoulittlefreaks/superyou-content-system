# content_generation/publisher.py

import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
wp_site = os.getenv("WP_SITE")
wp_user = os.getenv("WP_USER")
wp_app_password = os.getenv("WP_APP_PASSWORD")

def publish_post(wp_site, wp_user, wp_app_password, title, content, status='draft'):
    """
    Publishes a post to a WordPress site using the REST API.

    Args:
        wp_site (str): Base URL of the WordPress site (e.g., 'https://example.com')
        wp_user (str): WordPress username
        wp_app_password (str): Application password
        title (str): Title of the blog post
        content (str): Main content of the blog post
        status (str): Post status ('publish', 'draft', 'pending')
    """

    auth = HTTPBasicAuth(wp_user, wp_app_password)
    post = {
        'title': title,
        'content': content,
        'status': status,
    }

    try:
        response = requests.post(
            f"{wp_site}/wp-json/wp/v2/posts",
            auth=auth,
            json=post
        )

        if response.status_code == 201:
            print('✅ Post published successfully!')
            print('Post URL:', response.json().get('link'))
        else:
            print(f'❌ Failed to publish. Status code: {response.status_code}')
            print('Response:', response.content)

    except Exception as e:
        print(f"❌ Error publishing post: {e}")