from pathlib import Path
import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from kleenet.web.routers import artwork_route, filters_route, collection_route
from kleenet.database import DatabaseAccessor


class KleenetServer:

    GLOBAL_PREFIX = "/api/v1"

    @staticmethod
    def serve_from() -> tuple:
        """Get folders containing static files and templates"""
        basedir = Path(os.path.realpath(__file__)).parent
        templates = basedir / "templates"
        static = basedir / "static"
        return templates, static

    def __init__(self):

        self.servepath = KleenetServer.serve_from()
        self.templates = Jinja2Templates(directory=self.servepath[0])
        self.app = FastAPI()
        self.db = DatabaseAccessor()
        self._add_routers()
        self.allow_cors()

    def allow_cors(self):
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _add_routers(self):
        """Add all API routers"""
        self.app.include_router(artwork_route(self.db), tags=["Artworks"], prefix=KleenetServer.GLOBAL_PREFIX + "/artworks")
        self.app.include_router(filters_route(self.db), tags=["Filters"], prefix=KleenetServer.GLOBAL_PREFIX + "/filters")
        self.app.include_router(collection_route(self.db), tags=["Collections"], prefix=KleenetServer.GLOBAL_PREFIX + "/collections")
        self.app.mount("/static", StaticFiles(directory=self.servepath[1]), name="static")

    async def start(self):
        """Run the server"""
        config = uvicorn.Config(
            self.app,
            host="0.0.0.0",
            port=5000,
            lifespan="off",
            access_log=False
        )
        server = uvicorn.Server(config=config)
        server.install_signal_handlers = lambda: None
        await server.serve()
