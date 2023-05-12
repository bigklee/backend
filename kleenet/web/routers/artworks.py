from fastapi import APIRouter, Response, Cookie, status

from kleenet.models import Artwork, ArtworkCollection, SimpleMessage
from kleenet.database import DatabaseAccessor


def artwork_route(db: DatabaseAccessor) -> APIRouter:
    router = APIRouter()

    @router.get("/", responses={200: {"model": ArtworkCollection}})
    async def get_all_artworks(
            title_de: str | None = None,
            title_en: str | None = None,
            artist: str | None = None,
            year: int | None = None,
            work_no: str | None = None,
            width: float | None = None,
            height: float | None = None,
            keyword: str | None = None,
            linked_work: int | None = None,
            institution: str | None = None
    ) -> ArtworkCollection:
        collection = db.get_all(
            title_de,
            title_en,
            artist,
            year,
            work_no,
            width,
            height,
            keyword,
            linked_work,
            institution
        )
        print(keyword)
        return collection

    @router.get("/{artwork_id}", responses={200: {"model": Artwork}, 404: {"model": SimpleMessage}} )
    async def get_artwork_by_id(response: Response, artwork_id: int) -> Artwork|SimpleMessage:
        work = db.get_by_id(artwork_id)
        if work is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return SimpleMessage.not_found()
        return work
    return router
