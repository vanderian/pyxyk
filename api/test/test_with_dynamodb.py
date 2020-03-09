import pytest

from api.controllers.read_controller import get_liquidity_pools, get_token_swaps, get_swap_rate
from api.controllers.write_controller import add_liquidity, drain_liquidity, swap_tokens
from api.repository.liquidity_pools import LiquidityPools
from api.repository.token_swaps import TokenSwaps
from api.schema.liquidity_pool_schema import LiquidityPoolSchema
from api.test.util import mock_datetime_utcnow, MOCKED_DATETIME, parse_response_ok


# WARNING: make sure you have started dynamoDB locally
@pytest.fixture()
def setup(mocker):
    if LiquidityPools.exists():
        LiquidityPools.delete_table()
    LiquidityPools.create_table(read_capacity_units=1, write_capacity_units=1)
    if TokenSwaps.exists():
        TokenSwaps.delete_table()
    TokenSwaps.create_table(read_capacity_units=1, write_capacity_units=1)
    mock_datetime_utcnow(mocker)


def test_create_liquidity(setup):
    event = {'body': '{"tokenSymbol":"USD","poolNative":200,"poolToken":100}'}

    schema = LiquidityPoolSchema()
    lp = schema.loads(event['body'])
    expected = schema.dump(lp)

    response = add_liquidity(event, None)
    assert parse_response_ok(response) == expected


def test_add_liquidity(setup):
    event = {'body': '{"tokenSymbol":"USD","poolNative":200,"poolToken":100}'}

    schema = LiquidityPoolSchema()
    lp = schema.loads(event['body'])
    lp['pool_native'] = 400
    lp['pool_token'] = 200
    expected = schema.dump(lp)

    add_liquidity(event, None)
    response = add_liquidity(event, None)
    assert parse_response_ok(response) == expected


def test_drain_pool(setup):
    event = {'body': '{"tokenSymbol":"USD","poolNative":500,"poolToken":500}'}

    schema = LiquidityPoolSchema()
    lp = schema.loads(event['body'])
    LiquidityPools(**lp).save()
    lp['pool_token'] = 0
    lp['pool_native'] = 0
    expected = schema.dump(lp)

    response = drain_liquidity(event, None)
    assert parse_response_ok(response) == expected


def test_swap_native(setup):
    event = {'body': '{"tokenIn": "USD", "tokenOut": "XYK", "amount": 10}'}

    schema = LiquidityPoolSchema()
    lp = schema.load({'tokenSymbol': 'USD', 'poolNative': 1000, 'poolToken': 1000})
    LiquidityPools(**lp).save()
    expected = {"amountOut": 9.410599306587415, "tokenIn": "USD", "tokenOut": "XYK", "amountIn": 10.0,
                "createdAt": MOCKED_DATETIME}

    response = swap_tokens(event, None)
    assert parse_response_ok(response) == expected


def test_swap_token(setup):
    event = {'body': '{"tokenIn": "XYK", "tokenOut": "USD", "amount": 10}'}

    schema = LiquidityPoolSchema()
    lp = schema.load({'tokenSymbol': 'USD', 'poolNative': 1000, 'poolToken': 1000})
    LiquidityPools(**lp).save()
    expected = {"amountOut": 9.410599306587415, "tokenIn": "XYK", "tokenOut": "USD", "amountIn": 10.0,
                "createdAt": MOCKED_DATETIME}

    response = swap_tokens(event, None)
    assert parse_response_ok(response) == expected


def test_swap_token_to_token(setup):
    event = {'body': '{"tokenIn": "USD", "tokenOut": "EUR", "amount": 10}'}

    schema = LiquidityPoolSchema()
    lps = [
        schema.load({'tokenSymbol': 'USD', 'poolNative': 1000, 'poolToken': 1000}),
        schema.load({'tokenSymbol': 'EUR', 'poolNative': 1000, 'poolToken': 1000}),
    ]
    for lp in lps:
        LiquidityPools(**lp).save()
    expected = {"amountOut": 8.860852703664705, "tokenIn": "USD", "tokenOut": "EUR", "amountIn": 10.0,
                "createdAt": MOCKED_DATETIME}

    response = swap_tokens(event, None)
    assert parse_response_ok(response) == expected

    lps = [
        schema.load({'tokenSymbol': 'EUR', 'poolNative': 1009.4105993065874, 'poolToken': 991.1391472963353}),
        schema.load({'tokenSymbol': 'USD', 'poolNative': 990.5894006934126, 'poolToken': 1010}),
    ]
    expected = list(map(lambda lp: schema.dump(lp), lps))
    response = get_liquidity_pools(None, None)
    assert parse_response_ok(response) == expected


def test_read_pools(setup):
    expected = [
        {'tokenSymbol': 'ETH', 'poolNative': 100, 'poolToken': 10000},
        {'tokenSymbol': 'USD', 'poolNative': 1000, 'poolToken': 1000},
    ]
    schema = LiquidityPoolSchema()
    for lp in expected:
        LiquidityPools(**(schema.load(lp))).save()

    response = get_liquidity_pools(None, None)
    assert parse_response_ok(response) == expected


def test_swap_rate_token_to_token(setup):
    event = {'queryStringParameters': {'tokenIn': 'USD', 'tokenOut': 'EUR', 'amount': '10'}}

    schema = LiquidityPoolSchema()
    lps = [
        schema.load({'tokenSymbol': 'EUR', 'poolNative': 1000, 'poolToken': 1000}),
        schema.load({'tokenSymbol': 'USD', 'poolNative': 1000, 'poolToken': 1000}),
    ]
    for lp in lps:
        LiquidityPools(**lp).save()
    expected = {"amountOut": 8.860852703664705, "tokenIn": "USD", "tokenOut": "EUR", "amountIn": 10.0,
                "createdAt": MOCKED_DATETIME}

    response = get_swap_rate(event, None)
    assert parse_response_ok(response) == expected

    # pools should remain unchanged
    expected = list(map(lambda lp: schema.dump(lp), lps))
    response = get_liquidity_pools(None, None)
    assert parse_response_ok(response) == expected


def test_get_token_swaps(setup):
    swap = {'body': '{"tokenIn": "XYK", "tokenOut": "USD", "amount": 10}'}

    schema = LiquidityPoolSchema()
    lp = schema.load({'tokenSymbol': 'USD', 'poolNative': 1000, 'poolToken': 1000})
    LiquidityPools(**lp).save()

    expected = [
        {"amountOut": 9.230602556731242, "tokenIn": "XYK", "tokenOut": "USD", "amountIn": 10.0,
         "createdAt": MOCKED_DATETIME},
        {"amountOut": 9.410599306587415, "tokenIn": "XYK", "tokenOut": "USD", "amountIn": 10.0,
         "createdAt": MOCKED_DATETIME},
    ]

    swap_tokens(swap, None)
    swap_tokens(swap, None)
    response = get_token_swaps(None, None)

    assert parse_response_ok(response) == expected
