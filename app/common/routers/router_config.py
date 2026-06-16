from typing import Type, TypedDict

from app.common.base_api import BaseAPI


class RouteConfig(TypedDict):
    path: str
    cls: Type[BaseAPI]