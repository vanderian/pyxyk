import unittest
from decimal import Decimal

from api.models import LiquidityPool


class MyTestCase(unittest.TestCase):
    def test_something(self):
        json = {'amountNative': 100, 'amountSymbol': 200, 'symbol': 'USD'}
        lp = LiquidityPool.from_dict(json)
        self.assertEqual(lp.amount_symbol, Decimal(200))
        self.assertEqual(lp.amount_native, Decimal(100))
        self.assertEqual(lp.symbol, 'USD')


if __name__ == '__main__':
    unittest.main()
