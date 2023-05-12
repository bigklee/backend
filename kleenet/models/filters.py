from pydantic import BaseModel


class Filters(BaseModel):
    keywords: list[str]
    years: list[int]
