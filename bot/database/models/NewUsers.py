from pydantic import BaseModel


class NewUsers(BaseModel):
    user_id: int
    access_date: str
    access_time: str