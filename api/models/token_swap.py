# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from api.models.base_model_ import Model
from api import util


class TokenSwap(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, symbol_in: str=None, symbol_out: str=None, amount_in: float=None, amount_out: float=None, swap_date: datetime=None):  # noqa: E501
        """TokenSwap - a model defined in Swagger

        :param symbol_in: The symbol_in of this TokenSwap.  # noqa: E501
        :type symbol_in: str
        :param symbol_out: The symbol_out of this TokenSwap.  # noqa: E501
        :type symbol_out: str
        :param amount_in: The amount_in of this TokenSwap.  # noqa: E501
        :type amount_in: float
        :param amount_out: The amount_out of this TokenSwap.  # noqa: E501
        :type amount_out: float
        :param swap_date: The swap_date of this TokenSwap.  # noqa: E501
        :type swap_date: datetime
        """
        self.swagger_types = {
            'symbol_in': str,
            'symbol_out': str,
            'amount_in': float,
            'amount_out': float,
            'swap_date': datetime
        }

        self.attribute_map = {
            'symbol_in': 'symbolIn',
            'symbol_out': 'symbolOut',
            'amount_in': 'amountIn',
            'amount_out': 'amountOut',
            'swap_date': 'swapDate'
        }
        self._symbol_in = symbol_in
        self._symbol_out = symbol_out
        self._amount_in = amount_in
        self._amount_out = amount_out
        self._swap_date = swap_date

    @classmethod
    def from_dict(cls, dikt) -> 'TokenSwap':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The TokenSwap of this TokenSwap.  # noqa: E501
        :rtype: TokenSwap
        """
        return util.deserialize_model(dikt, cls)

    @property
    def symbol_in(self) -> str:
        """Gets the symbol_in of this TokenSwap.


        :return: The symbol_in of this TokenSwap.
        :rtype: str
        """
        return self._symbol_in

    @symbol_in.setter
    def symbol_in(self, symbol_in: str):
        """Sets the symbol_in of this TokenSwap.


        :param symbol_in: The symbol_in of this TokenSwap.
        :type symbol_in: str
        """
        if symbol_in is None:
            raise ValueError("Invalid value for `symbol_in`, must not be `None`")  # noqa: E501

        self._symbol_in = symbol_in

    @property
    def symbol_out(self) -> str:
        """Gets the symbol_out of this TokenSwap.


        :return: The symbol_out of this TokenSwap.
        :rtype: str
        """
        return self._symbol_out

    @symbol_out.setter
    def symbol_out(self, symbol_out: str):
        """Sets the symbol_out of this TokenSwap.


        :param symbol_out: The symbol_out of this TokenSwap.
        :type symbol_out: str
        """
        if symbol_out is None:
            raise ValueError("Invalid value for `symbol_out`, must not be `None`")  # noqa: E501

        self._symbol_out = symbol_out

    @property
    def amount_in(self) -> float:
        """Gets the amount_in of this TokenSwap.


        :return: The amount_in of this TokenSwap.
        :rtype: float
        """
        return self._amount_in

    @amount_in.setter
    def amount_in(self, amount_in: float):
        """Sets the amount_in of this TokenSwap.


        :param amount_in: The amount_in of this TokenSwap.
        :type amount_in: float
        """
        if amount_in is None:
            raise ValueError("Invalid value for `amount_in`, must not be `None`")  # noqa: E501

        self._amount_in = amount_in

    @property
    def amount_out(self) -> float:
        """Gets the amount_out of this TokenSwap.


        :return: The amount_out of this TokenSwap.
        :rtype: float
        """
        return self._amount_out

    @amount_out.setter
    def amount_out(self, amount_out: float):
        """Sets the amount_out of this TokenSwap.


        :param amount_out: The amount_out of this TokenSwap.
        :type amount_out: float
        """
        if amount_out is None:
            raise ValueError("Invalid value for `amount_out`, must not be `None`")  # noqa: E501

        self._amount_out = amount_out

    @property
    def swap_date(self) -> datetime:
        """Gets the swap_date of this TokenSwap.


        :return: The swap_date of this TokenSwap.
        :rtype: datetime
        """
        return self._swap_date

    @swap_date.setter
    def swap_date(self, swap_date: datetime):
        """Sets the swap_date of this TokenSwap.


        :param swap_date: The swap_date of this TokenSwap.
        :type swap_date: datetime
        """
        if swap_date is None:
            raise ValueError("Invalid value for `swap_date`, must not be `None`")  # noqa: E501

        self._swap_date = swap_date
