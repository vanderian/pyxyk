from marshmallow import ValidationError
from pynamodb.connection.base import Connection
from pynamodb.exceptions import TransactWriteError
from pynamodb.transactions import TransactWrite

from api import xyk
from api.controllers.encoder import ok_200, error, validation_error, bad_input, not_found
from api.repository.db import connection
from api.repository.liquidity_pools import LiquidityPools
from api.repository.token_swaps import TokenSwaps
from api.schema.liquidity_pool_schema import LiquidityPoolSchema
from api.schema.swap_input_schema import SwapInputSchema
from api.schema.token_swap_schema import TokenSwapSchema


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

        if pool_native == 0 or pool_token == 0:
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

    schema = SwapInputSchema()
    try:
        data = schema.loads(event['body'])
    except ValidationError as err:
        return validation_error(err)

    if data['token_in'] == xyk.NATIVE_SYMBOL:
        key = data['token_out']
        fn = xyk.native_to_token
    else:
        key = data['token_in']
        fn = xyk.token_to_native

    try:
        pool_in = LiquidityPools.get(key)
    except LiquidityPools.DoesNotExist:
        return not_found("token pair not found for '{}' symbol".format(key))

    if pool_in.pool_token == 0 or pool_in.pool_native == 0:
        return bad_input("bad input, native or token pool for '{}' token is drained to zero".format(key))

    new_pool_in, payout = fn(pool_in.as_dict(), data['amount'])

    # check whether we are doing token to token swap
    key = data['token_out']
    new_pool_out = None
    pool_out = None
    if data['token_in'] != xyk.NATIVE_SYMBOL and key != xyk.NATIVE_SYMBOL:
        try:
            pool_out = LiquidityPools.get(key)
        except LiquidityPools.DoesNotExist:
            return not_found("token pair not found for '{}' symbol".format(key))

        if pool_out.pool_token == 0 or pool_in.pool_native == 0:
            return bad_input("bad input, native or token pool for '{}' token is drained to zero".format(key))

        new_pool_out, payout = xyk.native_to_token(pool_out.as_dict(), payout)

    swap = TokenSwaps(amount_in=data['amount'], amount_out=payout, token_in=data['token_in'],
                      token_out=data['token_out'])

    try:
        with TransactWrite(connection=connection) as transaction:
            transaction.update(
                pool_in,
                actions=[
                    LiquidityPools.pool_native.set(new_pool_in['pool_native']),
                    LiquidityPools.pool_token.set(new_pool_in['pool_token']),
                ]
            )
            if pool_out is not None:
                transaction.update(
                    pool_out,
                    actions=[
                        LiquidityPools.pool_native.set(new_pool_out['pool_native']),
                        LiquidityPools.pool_token.set(new_pool_out['pool_token']),
                    ]
                )
            transaction.save(swap)

    except TransactWriteError as e:
        return error(409, 'conflict, pools updated during swap', e)

    schema = TokenSwapSchema()
    return ok_200(schema.dump(swap))
