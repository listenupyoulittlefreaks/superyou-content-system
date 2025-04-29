# Set up the full project structure and move files in place
mkdir -p content_generation tests data/input data/output config notebooks utils

# Move the downloaded files to their correct locations (run this from your project root)
mv publisher.py content_generation/
mv test_publish.py tests/

echo "✅ Project folders created and files placed successfully!"