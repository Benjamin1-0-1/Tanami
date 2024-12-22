# schemas.py

from marshmallow import Schema, fields, validate, ValidationError

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3))
    password = fields.Str(load_only=True, required=True)
    role = fields.Str(dump_only=True)


class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    publisher = fields.Str(validate=validate.Length(max=255))
    level = fields.Str(validate=validate.Length(max=50))
    isbn = fields.Str(validate=validate.Length(max=100))
    title = fields.Str(required=True, validate=validate.Length(max=500))
    price = fields.Float()
    status = fields.Str(validate=validate.Length(max=50))


class BookAuditSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int()
    book_id = fields.Int()
    action = fields.Str()
    old_data = fields.Str()
    new_data = fields.Str()
    timestamp = fields.DateTime()
