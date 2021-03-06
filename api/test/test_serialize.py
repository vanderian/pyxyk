from api.schema.liquidity_pool_schema import LiquidityPoolSchema


# we should also provide test for all the other schemas

def test_serialize_request():
    scheme = LiquidityPoolSchema()
    event = '{"tokenSymbol":"USD","poolNative":200,"poolToken":100}'
    lp = scheme.loads(event)
    assert 'token_symbol' in lp and 'pool_native' in lp and 'pool_token' in lp
