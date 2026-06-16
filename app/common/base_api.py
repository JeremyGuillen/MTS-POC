class BaseAPI:
    HAS_LIST_METHOD = True

    def __init__(self, auth: dict | None = None, url_id: str | None = None):
        self.auth = auth or {}
        self.url_id = url_id

    def list(self):
        raise NotImplementedError("'list' not implemented")

    def get(self, body: dict | None = None):
        raise NotImplementedError("'get' not implemented")

    def post(self, body: dict):
        raise NotImplementedError("'post' not implemented")

    def put(self, body: dict):
        raise NotImplementedError("'put' not implemented")

    def delete(self, body: dict | None = None):
        raise NotImplementedError("'delete' not implemented")