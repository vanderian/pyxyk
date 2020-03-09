from api.controllers.write_controller import add_liquidity
from api.repository.liquidity_pools import LiquidityPools
from api.schema.liquidity_pool_schema import LiquidityPoolSchema
from api.test.util import parse_response_ok


# update pool values, 'N' defines NumberAttribute
def update(self, *args, **kwargs):
    for action in kwargs['actions']:
        name = str(action.values[0])
        value = float(action.values[1].values[1].value['N'])
        op = action.values[1].format_string.format(getattr(self, name), value)
        setattr(self, name, eval(op))


def test_add_liquidity_pools(mocker):
    event = {'body': '{"tokenSymbol":"USD","poolNative":200,"poolToken":100}'}

    # we cannot mock behavior inside update so we return update values directly
    schema = LiquidityPoolSchema()
    lp = schema.loads(event['body'])

    mocker.patch('api.repository.liquidity_pools.LiquidityPools.save')
    mocker.patch.object(LiquidityPools, 'update', autospec=True, side_effect=update)
    mocker.patch('api.repository.liquidity_pools.LiquidityPools.get',
                 side_effect=[LiquidityPools.DoesNotExist, LiquidityPools(**lp)])

    lp['pool_native'] = 400
    lp['pool_token'] = 200
    expected = schema.dump(lp)

    add_liquidity(event, None)
    response = add_liquidity(event, None)
    assert parse_response_ok(response) == expected
