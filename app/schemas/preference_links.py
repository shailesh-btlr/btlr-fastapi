from typing import List
from pydantic import BaseModel


class PreferenceSurveyBase(BaseModel):
    heading: str
    subheading: str
    slug: str
    image_url: str
    preference_list: str
    business_id: int


class PreferenceSurvey(PreferenceSurveyBase):
    id: int


PreferenceSurveyList = List[PreferenceSurvey]
