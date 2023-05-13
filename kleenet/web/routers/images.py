from fastapi import APIRouter, Response, Cookie, status
from fastapi.responses import FileResponse

from kleenet.models import Artwork, ArtworkCollection, SimpleMessage
from kleenet.database import ImageProvider


def image_route(imgp: ImageProvider) -> APIRouter:
    router = APIRouter()

    @router.get(
        "/random",
        responses={
            200: {
                "content": {"image/jpg": {}},
                "description": "Random image",
            },
            404: {"model": SimpleMessage}}
    )
    async def get_random(response: Response) -> FileResponse:
        file = imgp.get_random()
        if file is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return SimpleMessage.not_found()
        return FileResponse(file)

    return router
