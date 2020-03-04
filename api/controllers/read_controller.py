import connexion
import six

from api.models.liquidity_pool import LiquidityPool  # noqa: E501
from api.models.swap_input import SwapInput  # noqa: E501
from api.models.token_swap import TokenSwap  # noqa: E501
from api import util


def get_liquidity():  # noqa: E501
    """get swap pairs

    Get existing swap pairs with pools # noqa: E501


    :rtype: List[LiquidityPool]
    """
    return 'do some magic!'


def get_token_swaps():  # noqa: E501
    """get token swaps

    Get existing token swaps # noqa: E501


    :rtype: List[TokenSwap]
    """
    return 'do some magic!'


def rate_tokens(body=None):  # noqa: E501
    """get swap rate without updating pools

    Get token swap rate defined by in &amp; out symbols and input amount # noqa: E501

    :param body: tokens to get rate with amount
    :type body: dict | bytes

    :rtype: TokenSwap
    """
    if connexion.request.is_json:
        body = SwapInput.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
