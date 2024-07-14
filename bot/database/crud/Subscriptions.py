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
    )
    session.add(new_users)
    session.commit()


def user_in_database(user_id: int):
    session = sessionmaker(engine)()
    query = session.query(SubscriptionsDB).filter_by(
        user_id=user_id
    ).first()
    return query is not None


def edit_subscription(user_id: int, new_days: int, ):
    session = sessionmaker(engine)()
    query = session.query(SubscriptionsDB).filter_by(user_id=user_id).first()
    query.subscription_days = new_days
    session.commit()


def get_subscription(user_id: int):
    session = sessionmaker(engine)()
    query = session.query(SubscriptionsDB).filter_by(user_id=user_id).first()
    return query.subscription_date, query.subscription_time

def get_time(user_id: int):
    session = sessionmaker(engine)()
    query = session.query(SubscriptionsDB).filter_by(user_id=user_id).first()
    all_time = query.subscription_date.split('-') + query.subscription_time.split(':')
    current_time = datetime.datetime.now()
    last_time=datetime.datetime(year=int(all_time[0]), month=int(all_time[1]), day=int(all_time[2]), hour=int(all_time[3]), minute=int(all_time[4]), second=int(all_time[5]))
    max_time = last_time+datetime.timedelta(days=query.subscription_days)
    return str(max_time-current_time).split('.')[0]


def is_subscribed(user_id):
    session = sessionmaker(engine)()
    query = session.query(SubscriptionsDB).filter_by(user_id=user_id).first()
    try:
        all_time = query.subscription_date.split('-')+query.subscription_time.split(':')
        logging.info(F"{all_time}")
        current_time = datetime.datetime.now()
        if (current_time-datetime.datetime(int(all_time[0]), int(all_time[1]), int(all_time[2]), int(all_time[3]), int(all_time[4]), int(all_time[5]))).seconds > (query.subscription_days*86400):  #y m d h m s
            return False
        return True
    except:
        return False


