from marshmallow import ValidationError

from app.common.base_api import BaseAPI
from app.core.database import SessionLocal
from app.repositories.mold_repository import MoldRepository
from app.schemas.mold_schema import MoldSchema
from app.services.molds_service import MoldService


class MoldsAPI(BaseAPI):
    def list(self):
        db = SessionLocal()

        try:
            repository = MoldRepository(db)
            service = MoldService(repository)

            molds = service.list_molds()
            schema = MoldSchema(many=True)

            return schema.dump(molds)

        finally:
            db.close()

    def post(self, body: dict):
        db = SessionLocal()

        try:
            name = body.get("name")
            entry_date = body.get("entry_date")

            if not name:
                raise ValueError("name is required")

            if not entry_date:
                raise ValueError("entry_date is required")

            repository = MoldRepository(db)
            service = MoldService(repository)

            mold = service.create_mold(
                name=name,
                entry_date=entry_date,
            )

            schema = MoldSchema()

            return schema.dump(mold)

        except ValidationError as error:
            raise ValueError(error.messages)

        finally:
            db.close()