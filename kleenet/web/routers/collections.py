from fastapi import APIRouter, Response, Cookie, status

from kleenet.models import Collection, CollectionList, SimpleMessage
from kleenet.database import DatabaseAccessor


def collection_route(db: DatabaseAccessor) -> APIRouter:
    router = APIRouter()

    @router.get("/", responses={200: {"model": CollectionList}})
    async def get_all_collections() -> CollectionList:
        collections = db.get_collections(collection_id=None)
        return collections

    @router.get("/{collection_id}", responses={200: {"model": Collection}, 404: {"model": SimpleMessage}} )
    async def get_artwork_by_id(response: Response, collection_id: int) -> Collection|SimpleMessage:
        work = db.get_collections(collection_id)
        if work is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return SimpleMessage.not_found()
        return work
    return router
