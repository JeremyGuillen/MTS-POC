# app/schemas/mold_schema.py
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models.mold import Mold


class MoldSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Mold
        load_instance = False
        include_fk = True
