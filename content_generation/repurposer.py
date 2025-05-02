import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def repurpose_blog(blog_post):
    if not blog_post:
        return None

    prompt = f"""
You are a content repurposing assistant for an NDIS therapy provider. Take the following blog post and:

1. Write a 200-word social media post that highlights its value to readers. Use an encouraging, inclusive tone.
2. Write a short email newsletter version including a subject line and 2–3 sentence preview.
3. Start each section with a clear label: SOCIAL MEDIA POST: and EMAIL: respectively.

BLOG POST:
{blog_post}
"""

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You help therapists repurpose content for social and email."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        return (response.choices[0].message.content or "").strip()
    except Exception as e:
        print("❌ Error repurposing blog post:", e)
        return None