from pydantic import BaseModel


class Insight(BaseModel):
    recommendation: str
    task_list: str


class DebugInsight(Insight):
    prompt: str
