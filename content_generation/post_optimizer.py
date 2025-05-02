# content_generation/post_optimizer.py

from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def optimize_post(content):
    prompt = f"""
    Analyze the following blog post and return:
    1. A catchy blog post title
    2. A 2-sentence meta description (SEO friendly)
    3. 3 FAQs with answers
    4. 5 keyword tags

    Blog Post:
    {content}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content
    except Exception as e:
        print("❌ Error optimizing post:", e)
        return None