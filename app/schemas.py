from marshmallow import Schema, fields

class BookSchema(Schema):
    id = fields.Integer()
    title = fields.String()
    author = fields.String()
    text = fields.String()