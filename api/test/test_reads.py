from api.controllers.read_controller import get_liquidity_pools, get_swap_rate, get_token_swaps
from api.repository.liquidity_pools import LiquidityPools
from api.repository.token_swaps import TokenSwaps
from api.schema.liquidity_pool_schema import LiquidityPoolSchema
from api.schema.token_swap_schema import TokenSwapSchema
from api.test.util import parse_response_ok, mock_datetime_utcnow, MOCKED_DATETIME


def test_get_liquidity_pools(mocker):
    expected = [
        {'tokenSymbol': 'ETH', 'poolNative': 100, 'poolToken': 10000},
        {'tokenSymbol': 'USD', 'poolNative': 1000, 'poolToken': 1000},
    ]
    schema = LiquidityPoolSchema()

    mock = mocker.patch('api.repository.liquidity_pools.LiquidityPools.scan')
    mock.return_value = list(map(lambda lp: LiquidityPools(**schema.load(lp)), expected))

    response = get_liquidity_pools(None, None)
    assert parse_response_ok(response) == expected


def test_get_swap_rate(mocker):
    event = {'queryStringParameters': {"tokenIn": "USD", "tokenOut": "EUR", "amount": 10}}

    schema = LiquidityPoolSchema()
    lps = [
        schema.load({'tokenSymbol': 'USD', 'poolNative': 1000, 'poolToken': 1000}),
        schema.load({'tokenSymbol': 'EUR', 'poolNative': 1000, 'poolToken': 1000}),
    ]
    mock_datetime_utcnow(mocker)
    mock = mocker.patch('api.repository.liquidity_pools.LiquidityPools.get')
    mock.side_effect = list(map(lambda lp: LiquidityPools(**lp), lps))
    expected = {"amountOut": 8.860852703664705, "tokenIn": "USD", "tokenOut": "EUR", "amountIn": 10.0,
                "createdAt": MOCKED_DATETIME}

    response = get_swap_rate(event, None)
    assert parse_response_ok(response) == expected


def test_get_token_swaps(mocker):
    expected = [
        {"amountOut": 9.230602556731242, "tokenIn": "XYK", "tokenOut": "USD", "amountIn": 10.0,
         "createdAt": MOCKED_DATETIME},
        {"amountOut": 9.410599306587415, "tokenIn": "XYK", "tokenOut": "USD", "amountIn": 10.0,
         "createdAt": MOCKED_DATETIME},
    ]
    schema = TokenSwapSchema()
    mock_list = list(map(lambda ts: TokenSwaps(**schema.load(ts)), expected))
    mock_datetime_utcnow(mocker)
    mock_result = mocker.patch('pynamodb.pagination.ResultIterator')
    mock_result.last_evaluated_key = None
    mock_result.__iter__.return_value = iter(mock_list)
    mocker.patch('api.repository.token_swaps.TokenSwaps.scan', return_value=mock_result)

    response = get_token_swaps({}, None)
    parsed = parse_response_ok(response)

    assert parsed.get('nextPageId') is None
    assert parsed['items'] == expected
