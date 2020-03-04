from decimal import Decimal

from api.models import LiquidityPool

FEE = Decimal(0.25)
SYMBOL = "XYK"


def native_to_token(lp: LiquidityPool, amount: Decimal):
    invariant = lp.amount_native * lp.amount_symbol
    fee = amount * FEE
    native_pool = lp.amount_native + amount
    token_pool = invariant / (native_pool - fee)
    payout = lp.amount_symbol - token_pool
    return LiquidityPool(lp.symbol, native_pool, token_pool), payout


def token_to_native(lp: LiquidityPool, amount: Decimal):
    invariant = lp.amount_native * lp.amount_symbol
    fee = amount * FEE
    token_pool = lp.amount_symbol + amount
    native_pool = invariant / (token_pool - fee)
    payout = lp.amount_native - native_pool
    return LiquidityPool(lp.symbol, native_pool, token_pool), payout


def token_to_token(lp_in: LiquidityPool, lp_out: LiquidityPool, amount: Decimal):
    in_pool, native_payout = token_to_native(lp_in, amount)
    out_pool, token_payout = native_to_token(lp_out, native_payout)
    return in_pool, out_pool, token_payout
