import json

from marshmallow import ValidationError

from api.controllers.encoder import ok_200, validation_error, bad_input, not_found, create_response
from api.controllers.swap import make_swap
from api.repository.liquidity_pools import LiquidityPools
from api.schema.liquidity_pool_schema import LiquidityPoolSchema


def create_response(code: int, body):
    return {'statusCode': code, 'body': json.dumps(body)}


def ok_200(body):
    return create_response(200, body)


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

    pool.refresh()

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
