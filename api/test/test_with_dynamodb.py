import json

import pytest

from api.controllers.read_controller import get_liquidity_pools
from api.controllers.write_controller import add_liquidity, drain_liquidity, swap_tokens
from api.repository.liquidity_pools import LiquidityPools
# WARNING: make sure you have started dynamoDB locally
from api.repository.token_swaps import TokenSwaps
from api.schema.liquidity_pool_schema import LiquidityPoolSchema


@pytest.fixture()
def setup():
    if LiquidityPools.exists():
        LiquidityPools.delete_table()
    LiquidityPools.create_table(read_capacity_units=1, write_capacity_units=1)
    if TokenSwaps.exists():
        TokenSwaps.delete_table()
    TokenSwaps.create_table(read_capacity_units=1, write_capacity_units=1)


def assert200(response, expected):
    status = response['statusCode']
    data = json.loads(response['body'])
    assert status == 200 and data == expected


def test_create_liquidity(setup):
    event = {'body': '{"tokenSymbol":"USD","poolNative":200,"poolToken":100}'}

    schema = LiquidityPoolSchema()
    lp = schema.loads(event['body'])
    expected = schema.dump(lp)

    response = add_liquidity(event, None)
    assert200(response, expected)


def test_add_liquidity(setup):
    event = {'body': '{"tokenSymbol":"USD","poolNative":200,"poolToken":100}'}

    schema = LiquidityPoolSchema()
    lp = schema.loads(event['body'])
    lp['pool_native'] = 400
    lp['pool_token'] = 200
    expected = schema.dump(lp)

    add_liquidity(event, None)
    response = add_liquidity(event, None)
    assert200(response, expected)


def test_read_pools(setup):
    expected = [
        {'tokenSymbol': 'ETH', 'poolNative': 100, 'poolToken': 10000},
        {'tokenSymbol': 'USD', 'poolNative': 1000, 'poolToken': 1000},
    ]
    schema = LiquidityPoolSchema()
    for lp in expected:
        LiquidityPools(**(schema.load(lp))).save()

    pools = get_liquidity_pools(None, None)
    assert200(pools, expected)


def test_drain_pool(setup):
    event = {'body': '{"tokenSymbol":"USD","poolNative":500,"poolToken":500}'}

    schema = LiquidityPoolSchema()
    lp = schema.loads(event['body'])
    LiquidityPools(**lp).save()
    lp['pool_token'] = 0
    lp['pool_native'] = 0
    expected = schema.dump(lp)

    response = drain_liquidity(event, None)
    assert200(response, expected)


def test_swap_native(setup):
    event = {'body': '{"tokenIn": "USD", "tokenOut": "XYK", "amount": 10}'}

    schema = LiquidityPoolSchema()
    lp = schema.load({'tokenSymbol': 'USD', 'poolNative': 1000, 'poolToken': 1000})
    LiquidityPools(**lp).save()
    expected = {"amountOut": 9.410599306587415, "tokenIn": "USD", "tokenOut": "XYK", "amountIn": 10.0}

    response = swap_tokens(event, None)
    status = response['statusCode']
    data = json.loads(response['body'])
    del data['createdAt']
    assert status == 200 and data == expected


def test_swap_token(setup):
    event = {'body': '{"tokenIn": "XYK", "tokenOut": "USD", "amount": 10}'}

    schema = LiquidityPoolSchema()
    lp = schema.load({'tokenSymbol': 'USD', 'poolNative': 1000, 'poolToken': 1000})
    LiquidityPools(**lp).save()
    expected = {"amountOut": 9.410599306587415, "tokenIn": "XYK", "tokenOut": "USD", "amountIn": 10.0}

    response = swap_tokens(event, None)
    status = response['statusCode']
    data = json.loads(response['body'])
    del data['createdAt']
    assert status == 200 and data == expected


def test_swap_token_to_token(setup):
    event = {'body': '{"tokenIn": "USD", "tokenOut": "EUR", "amount": 10}'}

    schema = LiquidityPoolSchema()
    lps = [
        schema.load({'tokenSymbol': 'USD', 'poolNative': 1000, 'poolToken': 1000}),
        schema.load({'tokenSymbol': 'EUR', 'poolNative': 1000, 'poolToken': 1000}),
    ]
    for lp in lps:
        LiquidityPools(**lp).save()
    expected = {"amountOut": 8.860852703664705, "tokenIn": "USD", "tokenOut": "EUR", "amountIn": 10.0}

    response = swap_tokens(event, None)
    status = response['statusCode']
    data = json.loads(response['body'])
    del data['createdAt']
    assert status == 200 and data == expected
