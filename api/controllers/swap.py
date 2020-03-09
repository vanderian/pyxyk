import uuid
from datetime import datetime

from dateutil.tz import tzutc
from marshmallow import ValidationError
from pynamodb.exceptions import TransactWriteError
from pynamodb.transactions import TransactWrite

from api import xyk
from api.controllers.encoder import not_found, bad_input, error, ok_200, validation_error
from api.repository.db import connection
from api.repository.liquidity_pools import LiquidityPools
from api.repository.token_swaps import TokenSwaps
from api.schema.swap_input_schema import SwapInputSchema
from api.schema.token_swap_schema import TokenSwapSchema


def make_swap(json_data, save: bool = False):
    schema = SwapInputSchema()
    try:
        data = schema.load(json_data)
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

    swap = TokenSwaps(id=str(uuid.uuid4()), amount_in=data['amount'], amount_out=payout, token_in=data['token_in'],
                      token_out=data['token_out'], created_at=datetime.now(tzutc()))

    if save:
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
