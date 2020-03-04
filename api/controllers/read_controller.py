from datetime import datetime

import connexion
import six

from api.models.liquidity_pool import LiquidityPool  # noqa: E501
from api.models.token_swap import TokenSwap  # noqa: E501
from api import util, db, xyk


def get_liquidity():  # noqa: E501
    """get swap pairs

    Get existing swap pairs with pools # noqa: E501


    :rtype: List[LiquidityPool]
    """
    r = db.tablePools.scan()

    return r["Items"]


def get_swap_rate(symbol_in, symbol_out, amount):  # noqa: E501
    """get swap rate

    Get token swap rate defined by in &amp; out symbols and input amount # noqa: E501

    :param symbol_in: symbol to convert from
    :type symbol_in: str
    :param symbol_out: symbol to convert to
    :type symbol_out: str
    :param amount: amount to convert
    :type amount: Decimal

    :rtype: TokenSwap
    """

    # todo handle not found errs
    # todo remove DRY with swap method
    if symbol_in == xyk.SYMBOL:
        key = symbol_out
        fn = xyk.native_to_token
    else:
        key = symbol_in
        fn = xyk.token_to_native

    lp_in = LiquidityPool.from_dict(db.tablePools.get_item(Key={'symbol': key})['Item'])
    new_lp_in, payout = fn(lp_in, amount)

    new_lp_out = None
    if symbol_in != xyk.SYMBOL and symbol_out != xyk.SYMBOL:
        lp_out = LiquidityPool.from_dict(db.tablePools.get_item(Key={'symbol': symbol_out})['Item'])
        new_lp_out, payout = xyk.native_to_token(lp_out, payout)

    return TokenSwap(symbol_in, symbol_out, amount, payout, datetime.utcnow())


def get_token_swaps():  # noqa: E501
    """get token swaps

    Get existing token swaps # noqa: E501


    :rtype: List[TokenSwap]
    """
    r = db.tableSwaps.scan()
    swaps = map(lambda i: TokenSwap.from_dict(i), r['Items'])
    return list(swaps)
