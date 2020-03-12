import json

from marshmallow import ValidationError

from api.controllers.encoder import ok_200, validation_error, bad_input, not_found
from api.controllers.swap import make_swap
from api.repository.liquidity_pools import LiquidityPools
from api.schema.liquidity_pool_schema import LiquidityPoolSchema

"""
by XYK design, there is a requirement that all modifications to LiquidityPools should be done in a sequential manner,
since `add` and `drain` should happen sporadically, we should be ok with optimistic locking and possible error responses
and we should therefore only consider optimizing the `swaps`
easiest solution would be to wrap all write handlers behind one lambda handler with limited concurrency
or we could handle the swaps async and aggregate into time+amount windows (eg. 100ms or <0.001% liquidity reached)
either way we could end up filling up the queue, introducing delays between swap posted and swap executed,
which may have a significant effect on the final swap rate
an optional `limit rate` on final swap rate, and/or `limit rate deviation` on swap rate change between posted and
 executed rates could be introduced into token swap request
"""


def add_liquidity(event, context):
    """adds liquidity pools for swap pair

    Deposit to liquidity pools for native/token pair for existing or new token symbol

    :param event: AWS ApiGateway http event
    :type event: dict
    :param context AWS Lambda context
    :type context: LambdaContext

    :rtype: dict
    """
    schema = LiquidityPoolSchema()

    try:
        data = schema.loads(event['body'])
    except ValidationError as err:
        return validation_error(err)

    try:
        pool = LiquidityPools.get(data['token_symbol'])
        pool.update(actions=[
            LiquidityPools.pool_native.set(LiquidityPools.pool_native + data['pool_native']),
            LiquidityPools.pool_token.set(LiquidityPools.pool_token + data['pool_token']),
        ])
    except LiquidityPools.DoesNotExist:
        pool = LiquidityPools(**data)
        pool.save()

    return ok_200(schema.dump(pool))


def drain_liquidity(event, context):
    """drain liquidity from swap pair pools

    Drain liquidity pools for native/token pair for existing symbol

    :param event: AWS ApiGateway http event
    :type event: dict
    :param context AWS Lambda context
    :type context: LambdaContext

    :rtype: dict
    """

    schema = LiquidityPoolSchema()

    try:
        data = schema.loads(event['body'])
    except ValidationError as err:
        return validation_error(err)

    try:
        pool = LiquidityPools.get(data['token_symbol'])
        pool_native = pool.pool_native - data['pool_native']
        pool_token = pool.pool_token - data['pool_token']

        if pool_native < 0 or pool_token < 0:
            return bad_input('bad input, not enough amount in pools')

        pool.update(actions=[
            LiquidityPools.pool_native.set(pool_native),
            LiquidityPools.pool_token.set(pool_token),
        ])
    except LiquidityPools.DoesNotExist:
        return not_found("token pair not found for '{}' symbol".format(data['token_symbol']))

    return ok_200(schema.dump(pool))


def swap_tokens(event, context):
    """swap tokens and update pools

    Swap tokens defined by in &amp; out symbols and input amount # noqa: E501

    :param event: AWS ApiGateway http event
    :type event: dict
    :param context AWS Lambda context
    :type context: LambdaContext

    :rtype: dict
    """
    return make_swap(json.loads(event['body']), True)
