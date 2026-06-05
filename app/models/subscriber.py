from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base


class Subscriber(Base):
    __tablename__ = "subscribers"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(
        String,
        unique=True,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )