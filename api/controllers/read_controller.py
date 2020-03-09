from api.controllers.encoder import ok_200
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

    Get token swap rate defined by in &amp; out symbols and input amount # noqa: E501

    :param symbol_in: symbol to convert from
    :type symbol_in: str
    :param symbol_out: symbol to convert to
    :type symbol_out: str
    :param amount: amount to convert
    :type amount: Decimal

    :rtype: TokenSwaps
    """
    print(event)
    return ok_200({})

#     # todo handle not found errs
#     # todo remove DRY with swap method
#     if symbol_in == xyk.SYMBOL:
#         key = symbol_out
#         fn = xyk.native_to_token
#     else:
#         key = symbol_in
#         fn = xyk.token_to_native
#
#     lp_in = LiquidityPool.from_dict(db.tablePools.get_item(Key={'symbol': key})['Item'])
#     new_lp_in, payout = fn(lp_in, amount)
#
#     new_lp_out = None
#     if symbol_in != xyk.SYMBOL and symbol_out != xyk.SYMBOL:
#         lp_out = LiquidityPool.from_dict(db.tablePools.get_item(Key={'symbol': symbol_out})['Item'])
#         new_lp_out, payout = xyk.native_to_token(lp_out, payout)
#
#     return TokenSwap(symbol_in, symbol_out, amount, payout, datetime.utcnow())
#
#
