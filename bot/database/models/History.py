from pydantic import BaseModel


class History(BaseModel):
    user_id: int
    about_business: str
    about_company: str
    about_audience: str
    names_and_descriptions: str
    marketing_strategy_plan: str
    lead_magnet: str
    pinned_post: str
    content_plan: str
    stories_content: str

