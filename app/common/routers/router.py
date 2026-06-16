import json
from abc import ABC, abstractmethod

from app.common.base_api import BaseAPI
from app.common.routers.route_config import RouteConfig


class BaseRouter(ABC):
    def __init__(self):
        self._routes: list[RouteConfig] = []
        self._route: str = ""
        self._method: str = ""
        self._body: dict | None = None
        self._auth: dict = {}
        self._api_route: str | None = None
        self._api_instance: BaseAPI | None = None

    @property
    def http_path(self):
        if not self._route.startswith("/"):
            return f"/{self._route}"

        return self._route

    @property
    def api_method(self):
        return self._method.lower()

    @property
    def url_id(self):
        if not self._api_route:
            return None

        clean_path = self.http_path.replace(self._api_route, "", 1).strip("/")
        return clean_path or None

    def _initialize_event(self, route, method, body, auth):
        self._route = route
        self._method = method
        self._body = body or {}
        self._auth = auth or {}
        self._api_route = None
        self._api_instance = None

    def _get_api_instance_and_path(self):
        sorted_routes = sorted(
            self._routes,
            key=lambda registered_route: len(registered_route["path"]),
            reverse=True,
        )

        for route in sorted_routes:
            route_path = route["path"]

            if self.http_path == route_path or self.http_path.startswith(f"{route_path}/"):
                self._api_route = route_path
                self._api_instance = route["cls"](
                    auth=self._auth,
                    url_id=self.url_id,
                )
                return self._api_instance

        return None

    def register_route(self, path: str, cls: type[BaseAPI]) -> None:
        clean_path = path if path.startswith("/") else f"/{path}"
        self._routes.append({"path": clean_path, "cls": cls})

    def _raise_not_found_message(self):
        return {
            "statusCode": 404,
            "body": json.dumps({"message": "Route not found"}),
        }

    @abstractmethod
    def execute(self, route, method, body, auth):
        raise NotImplementedError