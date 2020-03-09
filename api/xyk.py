SWAP_LIQUIDITY_FEE = 0.05
NATIVE_SYMBOL = "XYK"

'''
Prices are set automatically using the constant product (x*y=k) market maker mechanism, 
which keeps overall reserves in relative equilibrium. 
Reserves are pooled between a network of liquidity providers who supply the system with tokens 
in exchange for a proportional share of transaction fees. The exchange rate between XYK and an TOKEN is based on the 
relative sizes of their liquidity pools within the contract. 
This is done by maintaining the relationship pool_native * pool_token = invariant. 
This invariant is held constant during trades and only changes when liquidity is added or removed from the market.
'''


def native_to_token(lp: dict, amount: float):
    invariant = lp['pool_native'] * lp['pool_token']
    fee = amount * SWAP_LIQUIDITY_FEE
    native_pool = lp['pool_native'] + amount
    token_pool = invariant / (native_pool - fee)
    payout = lp['pool_token'] - token_pool
    return {'pool_native': native_pool, 'pool_token': token_pool}, payout


def token_to_native(lp: dict, amount: float):
    invariant = lp['pool_native'] * lp['pool_token']
    fee = amount * SWAP_LIQUIDITY_FEE
    token_pool = lp['pool_token'] + amount
    native_pool = invariant / (token_pool - fee)
    payout = lp['pool_native'] - native_pool
    return {'pool_native': native_pool, 'pool_token': token_pool}, payout

# def token_to_token(lp_in: LiquidityPool, lp_out: LiquidityPool, amount: Decimal):
#     in_pool, native_payout = token_to_native(lp_in, amount)
#     out_pool, token_payout = native_to_token(lp_out, native_payout)
#     return in_pool, out_pool, token_payout
