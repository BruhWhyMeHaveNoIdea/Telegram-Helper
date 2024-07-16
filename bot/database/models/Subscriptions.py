from pydantic import BaseModel


class Subscriptions(BaseModel):
    user_id: int
    subscription_date: str
    subscription_time: str
    subscription_days: int
    access_to_chats: bool
