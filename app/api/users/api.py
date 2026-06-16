from marshmallow import ValidationError

from app.common.base_api import BaseAPI
from app.core.database import SessionLocal
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreateSchema, UserSchema, UserUpdateSchema
from app.services.users_service import UserService


class UsersAPI(BaseAPI):
    def list(self):
        db = SessionLocal()

        try:
            repository = UserRepository(db)
            service = UserService(repository)

            users = service.list_users()
            schema = UserSchema(many=True)

            return schema.dump(users)

        finally:
            db.close()

    def get(self, body: dict | None = None):
        db = SessionLocal()

        try:
            if not self.url_id:
                raise ValueError("user id is required")

            repository = UserRepository(db)
            service = UserService(repository)

            user = service.get_user(self.url_id)
            schema = UserSchema()

            return schema.dump(user)

        finally:
            db.close()

    def post(self, body: dict):
        db = SessionLocal()

        try:
            data = UserCreateSchema().load(body or {})

            repository = UserRepository(db)
            service = UserService(repository)

            user = service.create_user(**data)
            schema = UserSchema()

            return schema.dump(user)

        except ValidationError as error:
            raise ValueError(error.messages)

        finally:
            db.close()

    def put(self, body: dict):
        db = SessionLocal()

        try:
            if not self.url_id:
                raise ValueError("user id is required")

            data = UserUpdateSchema().load(body or {}, partial=True)

            repository = UserRepository(db)
            service = UserService(repository)

            user = service.update_user(
                user_id=self.url_id,
                data=data,
            )

            schema = UserSchema()

            return schema.dump(user)

        except ValidationError as error:
            raise ValueError(error.messages)

        finally:
            db.close()

    def delete(self, body: dict | None = None):
        db = SessionLocal()

        try:
            if not self.url_id:
                raise ValueError("user id is required")

            repository = UserRepository(db)
            service = UserService(repository)

            return service.delete_user(self.url_id)

        finally:
            db.close()