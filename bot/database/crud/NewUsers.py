from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm import Session
from bot.database.database import engine
from bot.database.models.NewUsers import NewUsers
from bot.database.schemas.NewUsers import NewUsers as NewUsersDB
import datetime

def add_new_user(newuser: NewUsers):
    session = sessionmaker(engine)()
    new_users = NewUsersDB(
        user_id=newuser.user_id,
        access_time=newuser.access_time,
        access_date=newuser.access_date,
    )
    session.add(new_users)
    session.commit()

def user_in_database(user_id: int):
    session = sessionmaker(engine)()
    query = session.query(NewUsersDB).filter_by(
        user_id=user_id
    ).first()
    return query is not None

def get_user_join_time(user_id: int):
    session = sessionmaker(engine)()
    query = session.query(NewUsersDB).filter_by(user_id=user_id).first()
    return query.access_date, query.access_time
