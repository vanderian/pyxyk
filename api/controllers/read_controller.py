from api.controllers.encoder import ok_200
from api.controllers.swap import make_swap
from api.controllers.validation import parse_validate_with_schema, parse_condition, get_page_size_and_next_id
from api.repository.liquidity_pools import LiquidityPools
from api.repository.token_swaps import TokenSwaps
from api.schema.liquidity_pool_schema import LiquidityPoolSchema
from api.schema.token_swap_query_schema import TokenSwapsQuerySchema


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

    data, error = parse_validate_with_schema(TokenSwapsQuerySchema(), event.get('queryStringParameters', {}))
    if error is not None:
        return error

    condition = parse_condition(data)
    req_page_size, req_next_id = get_page_size_and_next_id(data)

    items, next_id = TokenSwaps.find_all(req_page_size, req_next_id, condition)

    response = {'items': items, 'nextPageId': next_id}
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
