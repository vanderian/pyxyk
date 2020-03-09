import json

from api.controllers.encoder import ok_200
from api.controllers.swap import make_swap
from api.repository.liquidity_pools import LiquidityPools
from api.repository.token_swaps import TokenSwaps
from api.schema.liquidity_pool_schema import LiquidityPoolSchema
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


def get_token_swaps(event, context):
    """get token swaps

    Get existing token swaps


    :rtype: dict
    """

    schema = TokenSwapSchema()
    r = TokenSwaps.scan()
    response = list(map(lambda ts: schema.dump(ts), r))

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
