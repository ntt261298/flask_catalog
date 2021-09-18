from marshmallow import Schema, fields, validate


class ItemSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1))
    content = fields.Str(required=True, validate=validate.Length(min=1))
    category_id = fields.Integer(required=True)


class UpdateItemSchema(Schema):
    title = fields.Str(required=True, validate=validate.Length(min=1))
    content = fields.Str(required=True, validate=validate.Length(min=1))
