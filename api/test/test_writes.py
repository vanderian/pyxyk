from pynamodb.expressions.operand import Value

from api.controllers.write_controller import add_liquidity, drain_liquidity
from api.repository.liquidity_pools import LiquidityPools
from api.schema.liquidity_pool_schema import LiquidityPoolSchema
from api.test.test_reads import test_get_swap_rate
from api.test.util import parse_response_ok


# update pool values, 'N' defines NumberAttribute
def update(self, *args, **kwargs):
    for action in kwargs['actions']:
        name = str(action.values[0])
        num_attr = action.values[1] if isinstance(action.values[1], Value) else action.values[1].values[1]
        value = float(num_attr.value['N'])
        op = action.values[1].format_string.format(value, getattr(self, name))
        setattr(self, name, eval(op))


def test_add_liquidity_pools(mocker):
    event = {'body': '{"tokenSymbol":"USD","poolNative":200,"poolToken":100}'}

    schema = LiquidityPoolSchema()
    lp = schema.loads(event['body'])
    pools_get = [LiquidityPools.DoesNotExist, LiquidityPools(**lp)]

    mocker.patch('api.repository.liquidity_pools.LiquidityPools.save')
    mocker.patch.object(LiquidityPools, 'update', autospec=True, side_effect=update)
    mocker.patch('api.repository.liquidity_pools.LiquidityPools.get', side_effect=pools_get)

    lp['pool_native'] = 400
    lp['pool_token'] = 200
    expected = schema.dump(lp)

    add_liquidity(event, None)
    response = add_liquidity(event, None)
    assert parse_response_ok(response) == expected


def test_drain_liquidity_pools(mocker):
    event = {'body': '{"tokenSymbol":"USD","poolNative":200,"poolToken":100}'}

    schema = LiquidityPoolSchema()
    lp = schema.loads(event['body'])

    mocker.patch.object(LiquidityPools, 'update', autospec=True, side_effect=update)
    mocker.patch('api.repository.liquidity_pools.LiquidityPools.get', return_value=LiquidityPools(**lp))

    lp['pool_native'] = 0
    lp['pool_token'] = 0
    expected = schema.dump(lp)

    response = drain_liquidity(event, None)
    assert parse_response_ok(response) == expected


# if we mock the transaction part this is the same as running without save for get_swap_rate
def test_token_swap(mocker):
    test_get_swap_rate(mocker)
