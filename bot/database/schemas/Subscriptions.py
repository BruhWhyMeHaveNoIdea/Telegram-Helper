from bot.database.database import Base
from sqlalchemy import Column, String, Integer


class Subscriptions(Base):
    __tablename__ = "Subscriptions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True, nullable=False)
    subscription_date = Column(String, unique=False, nullable=False)
    subscription_time = Column(String, unique=False, nullable=False)
    subscription_days = Column(Integer, unique=False, nullable=False)
