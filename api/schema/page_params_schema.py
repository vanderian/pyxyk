from marshmallow import fields, validate

from api.schema.camel_case_schema import CamelCasedSchema


class PageParamsSchema(CamelCasedSchema):
    # token swap item < 200B *1000 ~= 0,2MB per scan
    page_size = fields.Integer(required=False, validate=validate.Range(min=0, min_inclusive=False, max=1000))
    next_page_id = fields.Str(required=False)
