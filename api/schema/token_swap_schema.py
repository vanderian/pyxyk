from marshmallow import fields

from api.schema.camel_case_schema import CamelCasedSchema


class TokenSwapSchema(CamelCasedSchema):
    token_in = fields.Str(required=True)
    token_out = fields.Str(required=True)
    amount_in = fields.Float(required=True)
    amount_out = fields.Float(required=True)
    created_at = fields.DateTime(required=True)
