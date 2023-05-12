from pydantic import BaseModel

from kleenet.models import ArtworkCollection


class Collection:
    collection_id: int
    name: str
    author: str
    works: ArtworkCollection
