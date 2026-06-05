from sqlalchemy.orm import Session

from app.services.article_service import ingest_articles

from app.routes.newsletters import (
    rank_all,
    select_top_stories,
    summarize_top_stories,
    generate_newsletter
)


def run_pipeline(db: Session):

    print("Step 1: Ingesting articles...")
    ingest_result = ingest_articles(db)

    print("Step 2: Ranking articles...")
    rank_result = rank_all(db)

    print("Step 3: Selecting top stories...")
    top_stories_result = select_top_stories(db)

    print("Step 4: Summarizing top stories...")
    summary_result = summarize_top_stories(db)

    print("Step 5: Generating newsletter...")
    newsletter_result = generate_newsletter(db)

    return {
        "status": "success",
        "ingest": ingest_result,
        "ranking": rank_result,
        "top_stories": top_stories_result,
        "summaries": summary_result,
        "newsletter": newsletter_result
    }