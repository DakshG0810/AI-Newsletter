import feedparser
from datetime import datetime, timedelta

RSS_FEEDS = [

    # Hugging Face
    "https://huggingface.co/blog/feed.xml",

    # OpenAI
    "https://openai.com/news/rss.xml",

    # TechCrunch AI
    "https://techcrunch.com/category/artificial-intelligence/feed/",

    # VentureBeat AI
    "https://venturebeat.com/category/ai/feed/",

    # The Verge AI
    "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml",

    # Artificial Intelligence News
    "https://www.artificialintelligence-news.com/feed/",

    # MarkTechPost
    "https://www.marktechpost.com/feed/",

    # MIT Technology Review AI
    "https://www.technologyreview.com/topic/artificial-intelligence/feed/",

    # Google DeepMind Blog
    "https://deepmind.google/blog/rss.xml",

    # NVIDIA Blog
    "https://blogs.nvidia.com/feed/",

    # AWS Machine Learning Blog
    "https://aws.amazon.com/blogs/machine-learning/feed/",

    # Meta Engineering
    "https://engineering.fb.com/feed/",

    # Microsoft Research
    "https://www.microsoft.com/en-us/research/feed/",

    # Papers With Code
    "https://paperswithcode.com/rss/latest",

    # Analytics Vidhya
    "https://www.analyticsvidhya.com/feed/"
]

def fetch_articles():

    articles = []

    cutoff = datetime.utcnow() - timedelta(days=2)

    for feed_url in RSS_FEEDS:

        print(f"Fetching {feed_url}")

        feed = feedparser.parse(feed_url)

        print(f"Found {len(feed.entries)} entries")

        for entry in feed.entries:

            published = entry.get(
                "published_parsed"
            )

            if published:

                published_date = datetime(
                    *published[:6]
                )

                if published_date < cutoff:
                    continue

            articles.append({
                "title": entry.get("title"),
                "url": entry.get("link"),
                "source": feed.feed.get("title"),
                "published": published
            })

    print(
        f"Collected {len(articles)} recent articles"
    )

    return articles