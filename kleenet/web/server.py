from pathlib import Path
import os
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


class KleenetServer:

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
        self._add_routers()

    def _add_routers(self):
        """Add all API routers"""
        # self.app.include_router(redirect_route(), tags=["Redirect"])
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
