# app/handlers/molds_handler.py
import json

from app.core.database import SessionLocal
from app.repositories.mold_repository import MoldRepository
from app.schemas.mold_schema import MoldSchema
from app.services.molds_service import MoldService


def list_molds(event, context):
    db = SessionLocal()

    try:
        repository = MoldRepository(db)
        service = MoldService(repository)

        molds = service.list_molds()

        schema = MoldSchema(many=True)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps(schema.dump(molds), default=str),
        }

    finally:
        db.close()


def create_mold(event, context):
    db = SessionLocal()

    try:
        body = json.loads(event.get("body") or "{}")
        print(body)

        name = body.get("name")
        entry_date = body.get("entry_date")

        if not name:
            return {
                "statusCode": 400,
                "body": json.dumps({
                    "message": "name is required",
                }),
            }

        repository = MoldRepository(db)
        service = MoldService(repository)

        mold = service.create_mold(
            name=name,
            entry_date=entry_date
        )

        schema = MoldSchema()

        return {
            "statusCode": 201,
            "headers": {
                "Content-Type": "application/json",
            },
            "body": json.dumps(schema.dump(mold), default=str),
        }

    finally:
        db.close()
