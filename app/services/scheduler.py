from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from app.database import SessionLocal
from app.models.newsletter import Newsletter
from app.services.pipeline import run_pipeline

scheduler = BackgroundScheduler()


def daily_pipeline():

    db = SessionLocal()

    try:

        today = datetime.utcnow().date()

        existing_newsletter = (
            db.query(Newsletter)
            .filter(
                Newsletter.created_at >= datetime.combine(
                    today,
                    datetime.min.time()
                )
            )
            .first()
        )

        if existing_newsletter:

            print(
                "Newsletter already generated today. Skipping."
            )

            return

        print(
            "Running AI Newsletter pipeline..."
        )

        result = run_pipeline(db)

        print(
            f"Pipeline completed successfully: {result}"
        )

    except Exception as e:

        print(
            f"Pipeline failed: {e}"
        )

    finally:

        db.close()


def start_scheduler():

    scheduler.add_job(
        daily_pipeline,
        trigger="cron",
        hour=8,
        minute=0,
        id="daily_newsletter_pipeline",
        replace_existing=True
    )

    scheduler.start()

    print(
        "Scheduler started."
    )
    
