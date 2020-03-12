import pytest
from datetime import datetime, timedelta

from api.controllers.read_controller import get_liquidity_pools, get_token_swaps, get_swap_rate
from api.controllers.write_controller import add_liquidity, drain_liquidity, swap_tokens
from api.repository.liquidity_pools import LiquidityPools
from api.repository.token_swaps import TokenSwaps
from api.schema.liquidity_pool_schema import LiquidityPoolSchema
from api.test.util import mock_datetime_utcnow, MOCKED_DATETIME, parse_response_ok, sorted_ts, sorted_lp, \
    MOCKED_DATETIME_1


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


def test_read_pools(setup):
    expected = [
        {'tokenSymbol': 'ETH', 'poolNative': 100, 'poolToken': 10000},
        {'tokenSymbol': 'USD', 'poolNative': 1000, 'poolToken': 1000},
    ]
    schema = LiquidityPoolSchema()
    for lp in expected:
        LiquidityPools(**(schema.load(lp))).save()

    response = get_liquidity_pools(None, None)
    assert sorted_lp(parse_response_ok(response)) == sorted_lp(expected)


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


def test_get_token_swaps_with_paging(setup):
    event = {'queryStringParameters': {'pageSize': 1}}
    swap = {'body': '{"tokenIn": "XYK", "tokenOut": "USD", "amount": 10}'}

    schema = LiquidityPoolSchema()
    lp = schema.load({'tokenSymbol': 'USD', 'poolNative': 1000, 'poolToken': 1000})
    LiquidityPools(**lp).save()

    expected = [
        {"amountOut": 9.410599306587415, "tokenIn": "XYK", "tokenOut": "USD", "amountIn": 10.0,
         "createdAt": MOCKED_DATETIME},
        {"amountOut": 9.230602556731242, "tokenIn": "XYK", "tokenOut": "USD", "amountIn": 10.0,
         "createdAt": MOCKED_DATETIME_1},
    ]

    swap_tokens(swap, None)
    swap_tokens(swap, None)

    response = get_token_swaps(event, None)
    parsed = parse_response_ok(response)
    event = {'queryStringParameters': {'pageSize': 1, 'nextPageId': parsed['nextPageId']}}
    items = parsed['items']
    response = get_token_swaps(event, None)
    parsed = parse_response_ok(response)
    items += parsed['items']

    assert response.get('nextPageId') is None
    assert sorted_ts(items) == sorted_ts(expected)


def assert_count_for_query_param(q: dict, expected):
    event = {'queryStringParameters': q}
    response = get_token_swaps(event, None)
    parsed = parse_response_ok(response)
    assert len(parsed['items']) == expected


def test_get_token_swaps_with_queries(setup):
    swap = {'body': '{"tokenIn": "XYK", "tokenOut": "USD", "amount": 10}'}
    swap_inv = {'body': '{"tokenIn": "USD", "tokenOut": "XYK", "amount": 10}'}
    swap_eur = {'body': '{"tokenIn": "USD", "tokenOut": "EUR", "amount": 10}'}

    schema = LiquidityPoolSchema()
    lp = schema.load({'tokenSymbol': 'USD', 'poolNative': 1000, 'poolToken': 1000})
    LiquidityPools(**lp).save()
    lp = schema.load({'tokenSymbol': 'EUR', 'poolNative': 1000, 'poolToken': 1000})
    LiquidityPools(**lp).save()

    for i in range(0, 60):
        if i % 5 == 0:
            swap_tokens(swap_eur, None)
        elif i % 2 == 0:
            swap_tokens(swap, None)
        else:
            swap_tokens(swap_inv, None)

    dt = datetime.fromisoformat(MOCKED_DATETIME)
    day_1 = (dt + timedelta(days=20)).isoformat()
    day_2 = (dt + timedelta(days=40)).isoformat()

    assert_count_for_query_param({}, 60)
    assert_count_for_query_param({'tokenIn': 'XYK'}, 60 * 0.4)  # 40%
    assert_count_for_query_param({'tokenOut': 'USD'}, 60 * 0.4)  # 40%
    assert_count_for_query_param({'tokenIn': 'USD'}, 60 * 0.6)  # 40% + 20%
    assert_count_for_query_param({'tokenIn': 'XYK', 'tokenOut': 'EUR'}, 0)
    assert_count_for_query_param({'tokenIn': 'USD', 'tokenOut': 'EUR'}, 60 / 5),  # 20%
    assert_count_for_query_param({'tokenIn': 'USD', 'dateFrom': MOCKED_DATETIME}, 36)  # is inclusive
    assert_count_for_query_param({'tokenIn': 'USD', 'dateFrom': MOCKED_DATETIME_1}, 35)  # -1 on first day
    assert_count_for_query_param({'tokenIn': 'USD', 'dateTo': MOCKED_DATETIME}, 1)  # is inclusive
    assert_count_for_query_param({'tokenIn': 'USD', 'dateTo': MOCKED_DATETIME_1}, 2)
    assert_count_for_query_param({'tokenIn': 'XYK', 'dateFrom': day_1}, 40 * 0.4)  # 20->60 = 40 days span
    assert_count_for_query_param({'tokenIn': 'XYK', 'dateTo': day_2}, 40 * 0.4)  # 0->40  = 40 days span
    assert_count_for_query_param({'tokenIn': 'XYK', 'dateTo': day_1}, 20 * 0.4)  # 20d span
    assert_count_for_query_param({'tokenIn': 'XYK', 'dateFrom': day_2}, 20 * 0.4)  # 40->60 = 20d span
    assert_count_for_query_param({'tokenIn': 'XYK', 'dateFrom': day_1, 'dateTo': day_2}, 20 * 0.4)  # 20d span
    assert_count_for_query_param({'tokenIn': 'USD', 'tokenOut': 'EUR', 'dateFrom': day_1, 'dateTo': day_2}, 5)
