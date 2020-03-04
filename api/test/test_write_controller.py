# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from api.models.liquidity_pool import LiquidityPool  # noqa: E501
from api.models.swap_input import SwapInput  # noqa: E501
from api.models.token_swap import TokenSwap  # noqa: E501
from api.test import BaseTestCase


class TestWriteController(BaseTestCase):
    """WriteController integration test stubs"""

    def test_add_liquidity(self):
        """Test case for add_liquidity

        adds liquidity pools for swap pair
        """
        body = LiquidityPool()
        response = self.client.open(
            '/vanderian/pyxyk/1.0.0/liquidity/add',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_drain_liquidity(self):
        """Test case for drain_liquidity

        drain liquidity from swap pair pools
        """
        body = LiquidityPool()
        response = self.client.open(
            '/vanderian/pyxyk/1.0.0/liquidity/drain',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_swap_tokens(self):
        """Test case for swap_tokens

        swap tokens and update pools
        """
        body = SwapInput()
        response = self.client.open(
            '/vanderian/pyxyk/1.0.0/swap',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest

    unittest.main()
