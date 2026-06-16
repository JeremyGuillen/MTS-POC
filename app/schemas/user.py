from marshmallow import Schema, fields, validate
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models.user import User


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = False
        include_fk = True


class UserCreateSchema(Schema):
    first_name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
    )
    last_name = fields.String(
        required=True,
        validate=validate.Length(min=1, max=100),
    )
    email = fields.Email(required=True)
    phone = fields.String(
        required=False,
        allow_none=True,
        validate=validate.Length(max=30),
    )
    role = fields.String(
        required=False,
        load_default="user",
        validate=validate.Length(max=50),
    )
    status = fields.String(
        required=False,
        load_default="active",
        validate=validate.Length(max=50),
    )


class UserUpdateSchema(Schema):
    first_name = fields.String(
        required=False,
        validate=validate.Length(min=1, max=100),
    )
    last_name = fields.String(
        required=False,
        validate=validate.Length(min=1, max=100),
    )
    email = fields.Email(required=False)
    phone = fields.String(
        required=False,
        allow_none=True,
        validate=validate.Length(max=30),
    )
    role = fields.String(
        required=False,
        validate=validate.Length(max=50),
    )
    status = fields.String(
        required=False,
        validate=validate.Length(max=50),
    )