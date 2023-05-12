from pydantic import BaseModel

from kleenet.models import ArtworkCollection


class Collection(BaseModel):
    collection_id: int
    name: str
    author: str
    works: ArtworkCollection = ArtworkCollection(__root__=[])


class CollectionList(BaseModel):
    __root__: list[Collection]
