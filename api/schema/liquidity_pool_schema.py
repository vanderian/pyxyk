from marshmallow import fields, validate

from api.schema.camel_case_schema import CamelCasedSchema


class LiquidityPoolSchema(CamelCasedSchema):
    token_symbol = fields.Str(required=True, validate=validate.Length(max=12))
    pool_native = fields.Float(required=True, validate=validate.Range(min=0, min_inclusive=True))
    pool_token = fields.Float(required=True, validate=validate.Range(min=0, min_inclusive=True))
