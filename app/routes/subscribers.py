from fastapi import (
    APIRouter,
    Depends,
    HTTPException
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.subscriber import Subscriber
from app.schemas.subscriber import SubscriberCreate

from app.services.email_service import (
    send_welcome_email
)

router = APIRouter(
    prefix="/subscribers",
    tags=["Subscribers"]
)


@router.post("/")
def subscribe(
    subscriber: SubscriberCreate,
    db: Session = Depends(get_db)
):

    existing = (
    db.query(Subscriber)
    .filter(
        Subscriber.email == subscriber.email
    )
    .first()
    )
    print("EXISTING:", existing)
    if existing:

        if existing.is_active:

            raise HTTPException(
                status_code=400,
                detail="Email already subscribed"
            )

        existing.is_active = True

        db.commit()

        try:

            send_welcome_email(
                existing.email
            )

        except Exception as e:

            print(
                f"Welcome email failed: {e}"
            )

        return {
            "message": "Subscription reactivated",
            "email": existing.email
        }
    new_subscriber = Subscriber(
        email=subscriber.email
    )

    db.add(new_subscriber)

    db.commit()

    db.refresh(new_subscriber)

    try:

        send_welcome_email(
            new_subscriber.email
        )

    except Exception as e:

        print(
            f"Welcome email failed: {e}"
        )

    return {
        "message": "Subscribed successfully",
        "email": new_subscriber.email
    }


@router.get("/unsubscribe")
def unsubscribe(
    email: str,
    db: Session = Depends(get_db)
):

    subscriber = (
        db.query(Subscriber)
        .filter(
            Subscriber.email == email
        )
        .first()
    )

    if not subscriber:

        return {
            "success": False,
            "message": "Subscriber not found"
        }

    subscriber.is_active = False

    db.commit()

    return {
        "success": True,
        "message": f"{email} unsubscribed"
    }


@router.post("/send-welcome-email")
def send_test_welcome_email():

    result = send_welcome_email(
        "daksh0810@gmail.com"
    )

    return result