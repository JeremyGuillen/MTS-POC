from app.common.routers.router import BaseRouter


class MainRouter(BaseRouter):
    def __init__(self):
        super().__init__()

    def execute(self, route, method, body, auth=None):
        self._initialize_event(route, method, body, auth)

        api_instance = self._get_api_instance_and_path()

        if api_instance is None:
            return self._raise_not_found_message()

        method_name = self.api_method

        if method_name == "list" and not api_instance.HAS_LIST_METHOD:
            method_name = "get"

        method_to_execute = getattr(api_instance, method_name, None)

        if method_to_execute is None:
            raise ValueError(f"Method {method_name} is not supported for this route")

        if method_name == "list":
            return method_to_execute()

        return method_to_execute(body or {})