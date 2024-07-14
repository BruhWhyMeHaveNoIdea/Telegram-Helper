from bot.database.database import Base
from sqlalchemy import Column, String, Integer, Boolean

class History(Base):
    __tablename__ = "History"
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, unique=True, nullable=False)
    about_business = Column(Integer, unique=False, nullable=True)
    about_company = Column(String, unique=False, nullable=True)
    about_audience = Column(String, unique=False, nullable=True)
    names_and_descriptions = Column(String, nullable=True)
    marketing_strategy_plan = Column(String, nullable = True)
    lead_magnet = Column(String, nullable=True)
    pinned_post = Column(String, nullable=True)
    content_plan = Column(String, nullable=True)
    stories_content = Column(String, nullable=True)