from sqlalchemy.orm import Session

from app.services.article_service import ingest_articles
from app.services.ranker import rank_article
from app.services.summarizer import summarize_article
from app.models.article import Article


def run_pipeline(db: Session):

    results = {}

    # 1. Ingest
    results["ingest"] = ingest_articles(db)

    # TODO
    # rank articles

    # TODO
    # select top stories

    # TODO
    # summarize top stories

    # TODO
    # generate newsletter

    return results