from fastapi import APIRouter, Response, Cookie, status

from kleenet.models import Filters, SimpleMessage
from kleenet.database import DatabaseAccessor


def filters_route(db: DatabaseAccessor) -> APIRouter:
    router = APIRouter()

    @router.get("/", responses={200: {"model": Filters}})
    async def get_filters() -> Filters:
        return db.get_filters()

    return router
