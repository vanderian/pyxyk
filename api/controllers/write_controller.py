import uuid
from datetime import datetime

import connexion
import six

from api.models.liquidity_pool import LiquidityPool  # noqa: E501
from api.models.swap_input import SwapInput  # noqa: E501
from api.models.token_swap import TokenSwap  # noqa: E501
from api import util, db, xyk


def add_liquidity(body=None):  # noqa: E501
    """adds liquidity pools for swap pair

    Deposit to liqudity pools for native/token pair for existing or new token symbol   # noqa: E501

    :param body: Liquidity pool to add/update
    :type body: dict | bytes

    :rtype: LiquidityPool
    """
    if connexion.request.is_json:
        body = LiquidityPool.from_dict(connexion.request.get_json())  # noqa: E501

    r = db.tablePools.get_item(Key={'symbol': body.symbol})
    if 'Item' in r:
        it = LiquidityPool.from_dict(r['Item'])
        body.amount_native += it.amount_native
        body.amount_symbol += it.amount_symbol

    r = db.tablePools.put_item(Item=body.to_dict())

    return body


def drain_liquidity(body=None):  # noqa: E501
    """drain liquidity from swap pair pools

    Drain liqudity pools for native/token pair for existing symbol # noqa: E501

    :param body: Liquidity pool to drain
    :type body: dict | bytes

    :rtype: LiquidityPool
    """
    if connexion.request.is_json:
        body = LiquidityPool.from_dict(connexion.request.get_json())  # noqa: E501

    r = db.tablePools.get_item(Key={'symbol': body.symbol})
    if 'Item' in r:
        it = LiquidityPool.from_dict(r['Item'])
        body.amount_native = it.amount_native - body.amount_native
        body.amount_symbol = it.amount_symbol - body.amount_symbol
        if body.amount_symbol < 0 or body.amount_native < 0:
            return 'bad input, not enough amount in pools', 400
        else:
            r = db.tablePools.put_item(Item=body.to_dict())
            return body
    else:
        return "symbol's pool pair not found", 404


def swap_tokens(body=None):  # noqa: E501
    """swap tokens and update pools

    Swap tokens defined by in &amp; out symbols and input amount # noqa: E501

    :param body: tokens to swap with amount
    :type body: dict | bytes

    :rtype: TokenSwap
    """
    if connexion.request.is_json:
        body = SwapInput.from_dict(connexion.request.get_json())  # noqa: E501

    # todo handle not found errs
    if body.symbol_in == xyk.SYMBOL:
        key = body.symbol_out
        fn = xyk.native_to_token
    else:
        key = body.symbol_in
        fn = xyk.token_to_native

    lp_in = LiquidityPool.from_dict(db.tablePools.get_item(Key={'symbol': key})['Item'])
    new_lp_in, payout = fn(lp_in, body.amount)

    print(new_lp_in)
    print(payout)

    new_lp_out = None
    if body.symbol_in != xyk.SYMBOL and body.symbol_out != xyk.SYMBOL:
        lp_out = LiquidityPool.from_dict(db.tablePools.get_item(Key={'symbol': body.symbol_out})['Item'])
        new_lp_out, payout = xyk.native_to_token(lp_out, payout)
        db.tablePools.put_item(Item=new_lp_out.to_dict())

    db.tablePools.put_item(Item=new_lp_in.to_dict())

    swap = TokenSwap(body.symbol_in, body.symbol_out, body.amount, payout, datetime.utcnow())
    data = swap.to_dict()
    data['id'] = str(uuid.uuid1())
    data['swapDate'] = swap.swap_date.isoformat()
    print(data)
    db.tableSwaps.put_item(Item=data)

    return swap
