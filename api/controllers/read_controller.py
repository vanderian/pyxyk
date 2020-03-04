import connexion
import six

from api.models.liquidity_pool import LiquidityPool  # noqa: E501
from api.models.token_swap import TokenSwap  # noqa: E501
from api import util, db


def get_liquidity():  # noqa: E501
    """get swap pairs

    Get existing swap pairs with pools # noqa: E501


    :rtype: List[LiquidityPool]
    """
    r = db.tablePools.scan()

    return r["Items"]


def get_swap_rate(symbol_in, symbol_out, amount):  # noqa: E501
    """get swap rate

    Get token swap rate defined by in &amp; out symbols and input amount # noqa: E501

    :param symbol_in: symbol to convert from
    :type symbol_in: str
    :param symbol_out: symbol to convert to
    :type symbol_out: str
    :param amount: amount to convert
    :type amount: float

    :rtype: TokenSwap
    """
    return 'do some magic!'


def get_token_swaps():  # noqa: E501
    """get token swaps

    Get existing token swaps # noqa: E501


    :rtype: List[TokenSwap]
    """
    return 'do some magic!'
