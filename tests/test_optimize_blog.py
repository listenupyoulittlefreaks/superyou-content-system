# tests/test_optimize_blog.py

import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from content_generation.post_optimizer import optimize_post

# Load the generated blog post
input_path = os.path.join("data", "output", "generated_post.txt")
if not os.path.exists(input_path):
    print("❌ Blog post not found. Run test_generate_blog.py first.")
    exit()

with open(input_path, "r") as f:
    content = f.read()

# Run optimization
result = optimize_post(content)

# Save the result
if result:
    output_path = os.path.join("data", "output", "optimized_post.txt")
    with open(output_path, "w") as f:
        f.write(result)
    print(f"✅ Optimized content saved to: {output_path}")
else:
    print("❌ Failed to optimize post.")