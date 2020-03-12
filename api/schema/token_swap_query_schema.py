from marshmallow import fields

from api.schema.page_params_schema import PageParamsSchema


class TokenSwapsQuerySchema(PageParamsSchema):
    token_in = fields.Str(required=False)
    token_out = fields.Str(required=False)
    date_from = fields.DateTime(required=False)
    date_to = fields.DateTime(required=False)
