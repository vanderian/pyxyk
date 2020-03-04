# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from api.models.liquidity_pool import LiquidityPool  # noqa: E501
from api.models.swap_input import SwapInput  # noqa: E501
from api.models.token_swap import TokenSwap  # noqa: E501
from api.test import BaseTestCase


class TestReadController(BaseTestCase):
    """ReadController integration test stubs"""

    def test_get_liquidity(self):
        """Test case for get_liquidity

        get swap pairs
        """
        response = self.client.open(
            '/vanderian/pyxyk/1.0.0/liquidity/pools',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_token_swaps(self):
        """Test case for get_token_swaps

        get token swaps
        """
        response = self.client.open(
            '/vanderian/pyxyk/1.0.0/swaps',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_rate_tokens(self):
        """Test case for rate_tokens

        get swap rate without updating pools
        """
        body = SwapInput()
        response = self.client.open(
            '/vanderian/pyxyk/1.0.0/rate',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest

    unittest.main()
