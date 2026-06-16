import json

from marshmallow import ValidationError

from app.core.database import SessionLocal
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreateSchema, UserSchema, UserUpdateSchema
from app.services.users_service import UserService


def _json_response(status_code: int, body):
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps(body, default=str),
    }


def list_users(event, context):
    db = SessionLocal()

    try:
        repository = UserRepository(db)
        service = UserService(repository)

        users = service.list_users()
        schema = UserSchema(many=True)

        return _json_response(200, schema.dump(users))

    finally:
        db.close()


def get_user(event, context):
    db = SessionLocal()

    try:
        user_id = (event.get("pathParameters") or {}).get("id")

        if not user_id:
            return _json_response(400, {"message": "id is required"})

        repository = UserRepository(db)
        service = UserService(repository)

        user = service.get_user(user_id)
        schema = UserSchema()

        return _json_response(200, schema.dump(user))

    except ValueError as error:
        return _json_response(404, {"message": str(error)})

    finally:
        db.close()


def create_user(event, context):
    db = SessionLocal()

    try:
        body = json.loads(event.get("body") or "{}")
        data = UserCreateSchema().load(body)

        repository = UserRepository(db)
        service = UserService(repository)

        user = service.create_user(**data)
        schema = UserSchema()

        return _json_response(201, schema.dump(user))

    except ValidationError as error:
        return _json_response(400, {"message": error.messages})

    except ValueError as error:
        return _json_response(409, {"message": str(error)})

    finally:
        db.close()


def update_user(event, context):
    db = SessionLocal()

    try:
        user_id = (event.get("pathParameters") or {}).get("id")

        if not user_id:
            return _json_response(400, {"message": "id is required"})

        body = json.loads(event.get("body") or "{}")
        data = UserUpdateSchema().load(body, partial=True)

        repository = UserRepository(db)
        service = UserService(repository)

        user = service.update_user(user_id=user_id, data=data)
        schema = UserSchema()

        return _json_response(200, schema.dump(user))

    except ValidationError as error:
        return _json_response(400, {"message": error.messages})

    except ValueError as error:
        message = str(error)
        status_code = 409 if "email" in message else 404
        return _json_response(status_code, {"message": message})

    finally:
        db.close()


def delete_user(event, context):
    db = SessionLocal()

    try:
        user_id = (event.get("pathParameters") or {}).get("id")

        if not user_id:
            return _json_response(400, {"message": "id is required"})

        repository = UserRepository(db)
        service = UserService(repository)

        response = service.delete_user(user_id)

        return _json_response(200, response)

    except ValueError as error:
        return _json_response(404, {"message": str(error)})

    finally:
        db.close()