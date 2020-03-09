# todo error models
from marshmallow import fields

from api.schema.camel_case_schema import CamelCasedSchema


class ErrorResponse(CamelCasedSchema):
    status_code = fields.Number(required=True)
    message = fields.Str(required=True)
