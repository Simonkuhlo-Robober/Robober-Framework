from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .plugin import Plugin


class WebinterfaceExtension:
    def __init__(self, parent_plugin: "Plugin", custom_id:str = None, templates: Jinja2Templates = None):
        self.parent_plugin = parent_plugin
        self.router:"APIRouter" = APIRouter(prefix=f"/{custom_id}", tags=["extension", f"{self.parent_plugin.metadata.name}/{custom_id}"])
        self.templates = templates
        self.setup_router()

    def setup_router(self) -> None:
        pass