from sqlalchemy.orm import sessionmaker
from bot.database.database import engine
from bot.database.models.History import History
from bot.database.schemas.History import History as HistoryDB
import datetime

def add_new_user(history: History):
    session = sessionmaker(engine)()
    new_users = HistoryDB(
        user_id=history.user_id,
        about_business=history.about_business,
        about_company=history.about_company,
        about_audience=history.about_audience,
        names_and_descriptions = history.names_and_descriptions,
        marketing_strategy_plan = history.marketing_strategy_plan,
        lead_magnet = history.lead_magnet,
        pinned_post = history.pinned_post,
        content_plan = history.content_plan,
        stories_content = history.stories_content,
    )
    session.add(new_users)
    session.commit()
    session.close()

def user_in_database(user_id: int):
    session = sessionmaker(engine)()
    query = session.query(HistoryDB).filter_by(
        user_id=user_id
    ).first()
    session.close()
    return query is not None

def edit_history(id: int, new_business: str, new_company: str, new_audience: str, names_and_descriptions : str = None,marketing_strategy_plan : str = None,lead_magnet : str = None,\
                 pinned_post: str = None, content_plan : str = None, stories_content : str = None):
    session = sessionmaker(engine)()
    query = session.query(HistoryDB).filter_by(user_id=id).first()
    query.about_business = new_business
    query.about_company = new_company
    query.about_audience = new_audience
    query.names_and_descriptions = names_and_descriptions
    query.marketing_strategy_plan=marketing_strategy_plan
    query.lead_magnet=lead_magnet
    query.pinned_post=pinned_post
    query.content_plan=content_plan
    query.stories_content=stories_content
    session.commit()
    session.close()

def get_history(user_id: int):
    session = sessionmaker(engine)()
    query = session.query(HistoryDB).filter_by(user_id=user_id).first()
    session.close()
    return query.about_business, query.about_company, query.about_audience

def get_gpt_history(user_id: int):
    session = sessionmaker(engine)()
    query = session.query(HistoryDB).filter_by(user_id=user_id).first()
    session.close()
    return query.names_and_descriptions, query.marketing_strategy_plan, query.lead_magnet, query.pinned_post, query.content_plan, query.stories_content


def change_name(user_id:int, new_name:str):
    session = sessionmaker(engine)()
    query = session.query(HistoryDB).filter_by(user_id=user_id).first()
    query.names_and_descriptions = new_name
    session.close()

def change_marketing(user_id:int, new_marketing:str):
    session = sessionmaker(engine)()
    query = session.query(HistoryDB).filter_by(user_id=user_id).first()
    query.marketing_strategy_plan = new_marketing
    session.close()

def change_magnet(user_id:int, new_magnet:str):
    session = sessionmaker(engine)()
    query = session.query(HistoryDB).filter_by(user_id=user_id).first()
    query.lead_magnet = new_magnet
    session.close()

def change_ppost(user_id:int, new_post:str):
    session = sessionmaker(engine)()
    query = session.query(HistoryDB).filter_by(user_id=user_id).first()
    query.pinned_post = new_post
    session.close()

def change_content(user_id:int, new_plan:str):
    session = sessionmaker(engine)()
    query = session.query(HistoryDB).filter_by(user_id=user_id).first()
    query.content_plan = new_plan
    session.close()

def change_name(user_id:int, new_name:str):
    session = sessionmaker(engine)()
    query = session.query(HistoryDB).filter_by(user_id=user_id).first()
    query.names_and_descriptions = new_name
    session.close()

