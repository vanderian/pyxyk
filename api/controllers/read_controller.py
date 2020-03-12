from marshmallow import ValidationError, Schema
from pynamodb.pagination import ResultIterator

from api.controllers.encoder import ok_200, validation_error
from api.controllers.swap import make_swap
from api.repository.liquidity_pools import LiquidityPools
from api.repository.token_swaps import TokenSwaps
from api.schema.liquidity_pool_schema import LiquidityPoolSchema
from api.schema.page_params_schema import PageParamsSchema
from api.schema.token_swap_schema import TokenSwapSchema


def get_liquidity_pools(event, context):
    """get swap pairs

    Get existing swap pairs with pools


    :rtype: dict
    """

    schema = LiquidityPoolSchema()
    r = LiquidityPools.scan()
    response = list(map(lambda lp: schema.dump(lp), r))

    return ok_200(response)


def get_token_swaps(event: dict, context):
    """get token swaps

    Get existing token swaps


    :rtype: dict
    """

    schema = PageParamsSchema()
    try:
        data = schema.load(event.get('queryStringParameters', {}))
    except ValidationError as err:
        return validation_error(err)

    schema = TokenSwapSchema()
    req_page_size = data.get('page_size')
    req_next_id = data.get('next_page_id')
    items = []
    while True:
        # very inefficient, scan goes through all records; we should feed the data to elastic and query from there
        result = TokenSwaps.scan(limit=req_page_size, last_evaluated_key=req_next_id)
        items += list(map(lambda ts: schema.dump(ts), result))
        req_next_id = result.last_evaluated_key
        if len(items) == req_page_size or req_next_id is None:
            break

    response = {'items': items}
    if result.last_evaluated_key is not None:
        # ref: repository.token_swaps.TokenSwaps.id: UnicodeAttribute('S')
        response = dict({'nextPageId': result.last_evaluated_key['id']['S']}, **response)

    return ok_200(response)


def get_swap_rate(event, context):
    """get swap rate

    Get token swap rate defined by in &amp; out symbols and input amount

    :param event: AWS ApiGateway http event
    :type event: dict
    :param context AWS Lambda context
    :type context: LambdaContext

    :rtype: dict
    """
    return make_swap(event['queryStringParameters'])
