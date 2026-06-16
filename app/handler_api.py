import json

from app.router_api import base_router


def _json_response(status_code: int, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(body, default=str),
    }


def _get_route(event: dict) -> str:
    request_context = event.get("requestContext") or {}

    if "http" in request_context:
        return request_context["http"].get("path", "/")

    return event.get("path", "/")


def _get_method(event: dict) -> str:
    request_context = event.get("requestContext") or {}

    if "http" in request_context:
        return request_context["http"].get("method", "")

    return event.get("httpMethod", "")


def _get_body(event: dict, method: str):
    if method in ["GET", "DELETE"]:
        return event.get("queryStringParameters") or {}

    return json.loads(event.get("body") or "{}")


def _get_auth(event: dict):
    request_context = event.get("requestContext") or {}
    authorizer_context = (request_context.get("authorizer") or {}).get("lambda") or {}

    return {
        "email": authorizer_context.get("email", ""),
        "source_ip": (request_context.get("http") or {}).get("sourceIp", ""),
    }


def router(event, context):
    try:
        route = _get_route(event)
        method = _get_method(event).upper()
        body = _get_body(event, method)
        auth = _get_auth(event)

        router_method = method

        if method == "GET" and "/" not in route.replace("/", "", 1):
            router_method = "LIST"

        if method == "GET":
            # GET /users should list.
            # GET /users/{id} should get one item.
            route_parts = [part for part in route.split("/") if part]
            router_method = "LIST" if len(route_parts) == 1 else "GET"

        if router_method not in ["LIST", "GET", "POST", "PUT", "DELETE"]:
            return _json_response(
                400,
                {"message": f"Invalid HTTP method: {method}"},
            )

        data = base_router.execute(
            route=route,
            method=router_method,
            body=body,
            auth=auth,
        )

        if isinstance(data, dict) and "statusCode" in data and "body" in data:
            return data

        return _json_response(200, data)

    except ValueError as error:
        message = str(error)

        if "not found" in message.lower():
            status_code = 404
        elif "already exists" in message.lower():
            status_code = 409
        else:
            status_code = 400

        return _json_response(status_code, {"message": message})

    except Exception as error:
        return _json_response(
            400,
            {"message": f"Failed HTTP event: {error}"},
        )