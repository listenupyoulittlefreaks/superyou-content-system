# 🧠 Smart Content System

An AI-powered, modular content engine that automates the full blog lifecycle — from ideation to publishing and optimization.

---

## ✅ What It Does

This system:

1. **Generates full blog articles** using OpenAI
2. **Extracts SEO metadata, FAQs, and tags** from the post
3. **Publishes posts to WordPress** via REST API
4. **Stores all content locally for reuse and repurposing**
5. **Is ready to connect with Notion, Airtable, LinkedIn, and more**

---

## 📁 Folder Structure

```
superyou-content-system/
├── .env                     ← API keys for OpenAI + WordPress
├── requirements.txt         ← All dependencies
├── content_generation/
│   ├── blog_writer.py       ← Generates blog from a brief
│   ├── post_optimizer.py    ← SEO optimization layer
│   └── publisher.py         ← Publishes to WordPress
├── tests/
│   ├── test_generate_blog.py ← Runs blog generation
│   ├── test_optimize_blog.py ← Runs optimization
│   └── test_publish.py       ← Publishes the final post
├── data/
│   ├── input/               ← Future: feed structured briefs
│   └── output/
│       ├── generated_post.txt
│       └── optimized_post.txt
```

---

## 🔧 Setup Instructions

1. Clone the repo:
```bash
git clone https://github.com/your-username/superyou-content-system.git
cd superyou-content-system
```

2. Create your virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```
OPENAI_API_KEY=your_openai_key
WP_SITE=https://yourwebsite.com
WP_USER=your_wp_username
WP_APP_PASSWORD=your_wp_app_password
```

---

## 🚀 Usage

### Generate a Blog Post
```bash
python tests/test_generate_blog.py
```

### Optimize the Blog Post
```bash
python tests/test_optimize_blog.py
```

### Publish to WordPress
```bash
python tests/test_publish.py
```

---

## 📌 Roadmap Ideas

- ✅ Blog generation
- ✅ SEO optimization (title, meta, FAQs)
- ✅ WordPress integration
- ⏳ Notion/Airtable integration
- ⏳ Repurpose to social/email content
- ⏳ Image prompt generation (DALL·E)
- ⏳ Analytics feedback loop (GA/Search Console)

---

**Built with ❤️ by Elizabeth Clinen and GPT**