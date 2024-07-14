from bot.database.database import Base
from sqlalchemy import Column, String, Integer, Boolean

class NewUsers(Base):
    __tablename__ = "NewUsers"
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, unique=True, nullable=False)
    access_time = Column(String, unique=False, nullable=False)
    access_date = Column(String, unique=False, nullable=False)