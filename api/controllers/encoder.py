import json

from marshmallow import ValidationError


def create_response(code: int, body):
    return {'statusCode': code, 'body': json.dumps(body)}


def ok_200(body):
    return create_response(200, body)


def error(code, message=None, errors=None):
    if errors is None:
        errors = {}

    body = {'status_code': code, 'message': message, **errors}
    return create_response(code, body)


def validation_error(err: ValidationError):
    error(422, "input validation error", {"errors": err.messages})


def not_found(message):
    error(404, message)


def bad_input(message):
    error(400, message)
