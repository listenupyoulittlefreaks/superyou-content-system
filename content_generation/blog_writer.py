# content_generation/blog_writer.py

import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY



def generate_blog_post(brief):
    prompt = f"""
    Write a detailed, engaging blog post with the following details:
    - Title: {brief.get('title')}
    - Keywords: {', '.join(brief.get('keywords', []))}
    - Headings: {', '.join(brief.get('headings', []))}
    - Goal: {brief.get('goal')}
    
    Use H2 subheadings, bullet points where appropriate, and keep the tone friendly and informative.
    """

    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1200
        )

        return response.choices[0].message.content

    except Exception as e:
        print("❌ Error generating blog post:", e)
        return None