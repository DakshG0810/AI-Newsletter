from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()


def daily_pipeline():

    print(
        "Running AI Newsletter pipeline..."
    )

    # pipeline execution goes here


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