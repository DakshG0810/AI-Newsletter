from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services.ranker import rank_article
from app.database import get_db
from app.models.article import Article
from app.services.article_service import ingest_articles
from app.services.summarizer import summarize_article
from app.models.newsletter import Newsletter
from app.services.newsletter_generator import (
    generate_newsletter_content
)
from datetime import datetime, timedelta
from app.models.newsletter import Newsletter
from app.services.email_service import (
    send_newsletter_email
)
from app.models.subscriber import Subscriber
router = APIRouter(
    prefix="/news",
    tags=["News"]
)


@router.post("/ingest")
def ingest(
    db: Session = Depends(get_db)
):
    return ingest_articles(db)


@router.post("/summarize/{article_id}")
def summarize_news(
    article_id: int,
    db: Session = Depends(get_db)
):

    article = (
        db.query(Article)
        .filter(Article.id == article_id)
        .first()
    )

    if not article:
        return {"error": "Article not found"}

    summary = summarize_article(
        article.content[:5000]
    )

    article.summary = summary

    db.commit()

    return {
        "article_id": article.id,
        "summary": summary
    }


@router.get("/articles")
def get_articles(
    db: Session = Depends(get_db)
):

    articles = db.query(Article).all()

    return [
        {
            "id": article.id,
            "title": article.title,
            "source": article.source,
            "score": article.importance_score,
            "top_story": article.is_top_story,
            "has_summary": article.summary is not None
        }
        for article in articles
    ]


@router.get("/article/{article_id}")
def get_article(
    article_id: int,
    db: Session = Depends(get_db)
):

    article = (
        db.query(Article)
        .filter(Article.id == article_id)
        .first()
    )

    if not article:
        return {"error": "Article not found"}

    return {
        "id": article.id,
        "title": article.title,
        "content": article.content,
        "summary": article.summary
    }

@router.post("/rank-all")
def rank_all(
    db: Session = Depends(get_db)
):

    articles = (
        db.query(Article)
        .filter(
            Article.importance_score.is_(None)
        )
        .all()
    )

    if not articles:

        return {
            "success": 0,
            "failed": 0,
            "message": "No articles to rank"
        }

    try:

        print(
            f"Ranking {len(articles)} articles..."
        )

        scores = rank_article(
            articles
        )

        success = 0
        failed = 0

        for article in articles:

            score = scores.get(
                str(article.id)
            )

            if score is None:

                failed += 1
                continue

            article.importance_score = int(score)

            success += 1

        db.commit()

        return {
            "success": success,
            "failed": failed,
            "total_articles": len(articles)
        }

    except Exception as e:

        db.rollback()

        return {
            "error": str(e)
        }
    

@router.post("/select-top-stories")
def select_top_stories(
    db: Session = Depends(get_db)
):

    # Reset previous selections
    db.query(Article).update(
        {Article.is_top_story: False}
    )

    # Find latest newsletter
    latest_newsletter = (
        db.query(Newsletter)
        .order_by(
            Newsletter.created_at.desc()
        )
        .first()
    )

    # Only consider articles newer than last newsletter
    if latest_newsletter:

        cutoff = latest_newsletter.created_at

        print(
            f"Selecting articles after {cutoff}"
        )

    else:

        cutoff = (
            datetime.utcnow()
            - timedelta(days=1)
        )

        print(
            f"No previous newsletter found. Using cutoff {cutoff}"
        )

    # Select today's important stories
    articles = (
        db.query(Article)
        .filter(
            Article.importance_score >= 8,
            Article.published_at >= cutoff
        )
        .order_by(
            Article.importance_score.desc()
        )
        .all()
    )

    # Fallback if too few articles qualify
    if len(articles) < 5:

        articles = (
            db.query(Article)
            .filter(
                Article.importance_score != None,
                Article.published_at >= cutoff
            )
            .order_by(
                Article.importance_score.desc()
            )
            .limit(10)
            .all()
        )

    # Mark selected articles
    for article in articles:

        article.is_top_story = True

    db.commit()

    return {
        "selected": len(articles),
        "cutoff": cutoff,
        "article_ids": [
            article.id
            for article in articles
        ]
    }
    
@router.post("/summarize-top-stories")
def summarize_top_stories(
    db: Session = Depends(get_db)
):

    articles = (
        db.query(Article)
        .filter(
            Article.is_top_story == True
        )
        .all()
    )

    if not articles:

        return {
            "success": 0,
            "failed": 0,
            "message": "No top stories found"
        }

    try:

        print(
            f"Summarizing {len(articles)} top stories..."
        )

        summaries = summarize_article(
            articles
        )

        success = 0
        failed = 0

        for article in articles:

            summary = summaries.get(
                str(article.id)
            )

            if not summary:

                failed += 1
                continue

            article.summary = summary

            success += 1

        db.commit()

        return {
            "success": success,
            "failed": failed,
            "total_articles": len(articles)
        }

    except Exception as e:

        db.rollback()

        return {
            "error": str(e)
        }

@router.post("/generate-newsletter")
def generate_newsletter(
    db: Session = Depends(get_db)
):

    articles = (
        db.query(Article)
        .filter(
            Article.is_top_story == True
        )
        .all()
    )

    if not articles:

        return {
            "error": "No top stories found"
        }

    newsletter_content = (
        generate_newsletter_content(
            articles
        )
    )

    newsletter = Newsletter(
        title="Daily AI Newsletter",
        content=newsletter_content
    )

    db.add(newsletter)

    db.commit()

    db.refresh(newsletter)

    return {
        "newsletter_id": newsletter.id
    }
    
@router.get("/latest-newsletter")
def latest_newsletter(
    db: Session = Depends(get_db)
):

    newsletter = (
        db.query(Newsletter)
        .order_by(
            Newsletter.id.desc()
        )
        .first()
    )

    if not newsletter:

        return {
            "error": "No newsletter found"
        }

    return {
        "id": newsletter.id,
        "title": newsletter.title,
        "content": newsletter.content,
        "created_at": newsletter.created_at
    }

@router.get("/stats")
def get_stats(
    db: Session = Depends(get_db)
):

    return {
        "articles": db.query(Article).count(),

        "top_stories": (
            db.query(Article)
            .filter(
                Article.is_top_story == True
            )
            .count()
        ),

        "newsletters": (
            db.query(Newsletter)
            .count()
        )
    }

@router.get("/top-stories")
def get_top_stories(
    db: Session = Depends(get_db)
):

    articles = (
        db.query(Article)
        .filter(
            Article.is_top_story == True
        )
        .order_by(
            Article.importance_score.desc()
        )
        .all()
    )

    return [
        {
            "id": article.id,
            "title": article.title,
            "source": article.source,
            "score": article.importance_score,
            "summary": article.summary,
            "url": article.url
        }
        for article in articles
    ]

@router.post("/run-pipeline")
def run_pipeline(
    db: Session = Depends(get_db)
):
    # 1. Ingest
    ingest_result = ingest_articles(db)

    # 2. Rank
    rank_result = rank_all(db)

    # 3. Select top stories
    top_stories = select_top_stories(db)

    # 4. Summarize
    summary_result = summarize_top_stories(db)

    # 5. Generate newsletter
    newsletter = generate_newsletter(db)

    latest_newsletter = (
        db.query(Newsletter)
        .order_by(
            Newsletter.created_at.desc()
        )
        .first()
    )

    subscribers = (
        db.query(Subscriber)
        .filter(
            Subscriber.is_active == True
        )
        .all()
    )

    emails_sent = 0
    emails_failed = 0

    for subscriber in subscribers:

        try:

            result = send_newsletter_email(
                subscriber.email,
                latest_newsletter
            )

            if result["success"]:

                emails_sent += 1

            else:

                emails_failed += 1

        except Exception as e:

            emails_failed += 1

            print(
                f"Failed to send newsletter to "
                f"{subscriber.email}: {e}"
            )

    return {
        "status": "success",
        "ingest": ingest_result,
        "ranking": rank_result,
        "top_stories": top_stories,
        "summaries": summary_result,
        "newsletter": newsletter_result,
        "emails_sent": emails_sent,
        "emails_failed": emails_failed
    }

@router.post("/send-test-email")
def send_test_email(
    db: Session = Depends(get_db)
):

    newsletter = (
        db.query(Newsletter)
        .order_by(
            Newsletter.id.desc()
        )
        .first()
    )

    if not newsletter:

        return {
            "error": "No newsletter found"
        }

    result = send_newsletter_email(
        "prernaaa13@gmail.com",
        newsletter
    )

    return result
@router.get("/health")
def health():
    return {"status": "ok"}

@router.get("/preview-newsletter-links-only-for-testing")
def preview_newsletter_links(
    db: Session = Depends(get_db)
):

    articles = (
        db.query(Article)
        .filter(
            Article.is_top_story == True
        )
        .all()
    )

    content = generate_newsletter_content(
        articles
    )

    return {
        "content": content
    }

@router.post("/send-preview-email-test")
def send_preview_email(
    db: Session = Depends(get_db)
):

    articles = (
        db.query(Article)
        .filter(
            Article.is_top_story == True
        )
        .all()
    )

    content = generate_newsletter_content(
        articles
    )

    preview_newsletter = Newsletter(
        title="Preview Newsletter",
        content=content
    )

    result = send_newsletter_email(
        "daksh0810@gmail.com",
        preview_newsletter
    )

    return result