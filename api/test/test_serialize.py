import unittest
from decimal import Decimal

from api.models import LiquidityPool


class MyTestCase(unittest.TestCase):
    def test_serialize_request(self):
        json = {'amountNative': 100, 'amountSymbol': 200, 'symbol': 'USD'}
        lp = LiquidityPool.from_dict(json)
        self.assertEqual(lp.amount_symbol, Decimal(200))
        self.assertEqual(lp.amount_native, Decimal(100))
        self.assertEqual(lp.symbol, 'USD')

    def test_serialize_dynamodb(self):
        json = {'symbol': 'USD2', 'amountNative': Decimal('100'), 'amountSymbol': Decimal('200')}
        lp = LiquidityPool.from_dict(json)
        self.assertEqual(lp.amount_symbol, Decimal(200))
        self.assertEqual(lp.amount_native, Decimal(100))
        self.assertEqual(lp.symbol, 'USD2')

    def test_serialize_to_dict(self):
        lp = LiquidityPool('USD2', Decimal(100), Decimal(100))
        d = lp.to_dict()
        self.assertIn("symbol", d)
        self.assertIn("amountNative", d)
        self.assertIn("amountSymbol", d)
        self.assertEqual(lp, LiquidityPool.from_dict(d))


if __name__ == '__main__':
    unittest.main()
