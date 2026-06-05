from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, Integer
from app.database import Base


class Article(Base):

    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    source = Column(String)
    content = Column(Text)
    summary = Column(Text)
    published_at = Column(DateTime)

    importance_score = Column(Integer, nullable=True)

    is_top_story = Column(
        Boolean,
        default=False
    )

    