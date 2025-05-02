# content_generation/image_creator.py

import os
import openai
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_images(title, brief, output_dir="data/images", num_images=2):
    os.makedirs(output_dir, exist_ok=True)

    prompt = f"Create a visual concept representing the topic: '{title}'. Theme: {brief.get('category', '') or 'NDIS allied health'}. Style: soft colors, warm, professional, watercolor or flat design."

    try:
        for i in range(num_images):
            response = openai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            image_url = response.data[0].url
            image_response = requests.get(image_url)

            if image_response.status_code == 200:
                image_filename = f"{title.replace(' ', '_').lower()}_{i+1}.png"
                image_path = os.path.join(output_dir, image_filename)
                with open(image_path, "wb") as f:
                    f.write(image_response.content)
                print(f"🖼️ Image saved: {image_path}")
            else:
                print(f"⚠️ Failed to download image from: {image_url}")

        return True

    except Exception as e:
        print("❌ Image generation failed:", e)
        return False