from marshmallow import ValidationError, Schema

from api.controllers.encoder import validation_error
from api.repository.token_swaps import TokenSwaps


def parse_validate_with_schema(schema: Schema, source: dict):
    try:
        return schema.load(source), None
    except ValidationError as err:
        return None, validation_error(err)


# should be called with validated data
def get_page_size_and_next_id(paging: dict) -> (int, int):
    return paging.get('page_size'), paging.get('next_page_id')


# should be called with validated data
def parse_condition(data: dict):
    condition = None
    if 'token_in' in data:
        condition &= TokenSwaps.token_in == data['token_in']
    if 'token_out' in data:
        condition &= TokenSwaps.token_out == data['token_out']
    if 'date_from' in data:
        condition &= TokenSwaps.created_at >= data['date_from']
    if 'date_to' in data:
        condition &= TokenSwaps.created_at <= data['date_to']

    return condition
