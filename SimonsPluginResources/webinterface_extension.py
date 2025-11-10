import os
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .plugin import Plugin
    from fastapi.requests import Request


class WebinterfaceExtension:
    def __init__(self, parent_plugin: "Plugin", custom_id:str = None):
        self.parent_plugin = parent_plugin
        self.router:"APIRouter" = APIRouter(prefix=custom_id, tags=["extension", f"{self.parent_plugin.name}/{custom_id}"])
        self.setup_router()

    def setup_router(self) -> None:
        templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "static"))

        @self.router.get("/view", response_class=HTMLResponse)
        async def settings_interface(request: "Request"):
            return templates.TemplateResponse("view.j2", {"request": request})