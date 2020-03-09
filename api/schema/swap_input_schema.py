from marshmallow import fields, validate

from api.schema.camel_case_schema import CamelCasedSchema


class SwapInputSchema(CamelCasedSchema):
    token_in = fields.Str(required=True)
    token_out = fields.Str(required=True)
    amount = fields.Float(required=True, validate=validate.Range(min=0, min_inclusive=False))
