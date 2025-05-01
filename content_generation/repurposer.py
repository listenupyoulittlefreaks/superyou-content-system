# content_generation/repurposer.py

import openai
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def repurpose_blog(post_text):
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        prompt = f"""
You are a digital marketing assistant for a disability services provider. Repurpose the following blog post into:

1. A social media post (at least 200 words) suitable for LinkedIn or Instagram, with a helpful, informative tone and appropriate hashtags.
2. An email snippet with a subject line and short paragraph (100–150 words), plus a clear call to action to read the full blog.

BLOG POST:
{post_text}
"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=800
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        print("❌ Error during repurposing:", e)
        return None