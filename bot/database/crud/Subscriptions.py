from sqlalchemy.orm import sessionmaker
from bot.database.database import engine
from bot.database.models.Subscriptions import Subscriptions
from bot.database.schemas.Subscriptions import Subscriptions as SubscriptionsDB
import datetime
import logging


def add_new_user(newsub: Subscriptions):
    session = sessionmaker(engine)()
    new_users = SubscriptionsDB(
        user_id=newsub.user_id,
        subscription_date=newsub.subscription_date,
        subscription_time=newsub.subscription_time,
        subscription_days=newsub.subscription_days,
        access_to_chats=newsub.access_to_chats
    )
    session.add(new_users)
    session.commit()


def user_in_database(user_id: int):
    session = sessionmaker(engine)()
    query = session.query(SubscriptionsDB).filter_by(
        user_id=user_id
    ).first()
    return query is not None

def get_date(user_id: int):
    session = sessionmaker(engine)()
    query = session.query(SubscriptionsDB).filter_by(user_id=user_id).first()
    session.close()
    return query.subscription_date, query.subscription_time

def get_days(user_id: int):
    session = sessionmaker(engine)()
    query = session.query(SubscriptionsDB).filter_by(user_id=user_id).first()
    session.close()
    return query.subscription_days

def add_days(user_id: int, days: int, access_to_chats: bool):
    session = sessionmaker(engine)()
    query = session.query(SubscriptionsDB).filter_by(user_id=user_id).first()
    days_in_db = query.subscription_days
    query.subscription_days=(days_in_db+days)
    query.access_to_chats=access_to_chats
    session.commit()
    session.close()
