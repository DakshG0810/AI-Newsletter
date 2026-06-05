from sqlalchemy.orm import Session
from datetime import datetime

from app.models.article import Article
from app.services.rss_service import fetch_articles
from app.services.article_scraper import scrape_article


def ingest_articles(db: Session):

    articles = fetch_articles()

    added = 0

    for article in articles:

        existing = (
            db.query(Article)
            .filter(
                Article.url == article["url"]
            )
            .first()
        )

        if existing:
            continue

        print(
            f"Scraping: {article['title']}"
        )

        content = scrape_article(
            article["url"]
        )

        published_at = None

        if article.get("published"):

            published_at = datetime(
                *article["published"][:6]
            )

        db_article = Article(
            title=article["title"],
            url=article["url"],
            source=article["source"],
            content=content,
            published_at=published_at,
            summary=None,
            importance_score=None,
            is_top_story=False
        )

        db.add(db_article)

        added += 1

    db.commit()

    return {
        "articles_added": added
    }