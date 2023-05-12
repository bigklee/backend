from pydantic import BaseModel, validator, root_validator
import re


class Artwork(BaseModel):
    id: int
    title_de: str | None
    title_en: str | None
    artist: str | None
    year: int | None
    work_no: str | None
    width: float | None
    height: float | None
    mat_tech_de: str | None
    mat_tech_en: str | None
    keywords: list[str] | None
    linked_works: list[int] | None
    link_description: str | None
    institution: str | None

    @validator("keywords", always=True, pre=True)
    def split_keywords(cls, v):
        if v is None:
            return None
        val_list = v.split("/")
        return val_list

    @validator("linked_works", always=True, pre=True)
    def split_linked_ids(cls, v):
        if v is None:
            return None
        str_list = v.split("/")
        return [int(i) for i in str_list]


class ArtworkCollection(BaseModel):
    __root__: list[Artwork]
