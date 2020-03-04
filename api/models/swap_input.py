# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from api.models.base_model_ import Model
from api import util


class SwapInput(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, symbol_in: str=None, symbol_out: str=None, amount: float=None):  # noqa: E501
        """SwapInput - a model defined in Swagger

        :param symbol_in: The symbol_in of this SwapInput.  # noqa: E501
        :type symbol_in: str
        :param symbol_out: The symbol_out of this SwapInput.  # noqa: E501
        :type symbol_out: str
        :param amount: The amount of this SwapInput.  # noqa: E501
        :type amount: float
        """
        self.swagger_types = {
            'symbol_in': str,
            'symbol_out': str,
            'amount': float
        }

        self.attribute_map = {
            'symbol_in': 'symbolIn',
            'symbol_out': 'symbolOut',
            'amount': 'amount'
        }
        self._symbol_in = symbol_in
        self._symbol_out = symbol_out
        self._amount = amount

    @classmethod
    def from_dict(cls, dikt) -> 'SwapInput':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The SwapInput of this SwapInput.  # noqa: E501
        :rtype: SwapInput
        """
        return util.deserialize_model(dikt, cls)

    @property
    def symbol_in(self) -> str:
        """Gets the symbol_in of this SwapInput.


        :return: The symbol_in of this SwapInput.
        :rtype: str
        """
        return self._symbol_in

    @symbol_in.setter
    def symbol_in(self, symbol_in: str):
        """Sets the symbol_in of this SwapInput.


        :param symbol_in: The symbol_in of this SwapInput.
        :type symbol_in: str
        """
        if symbol_in is None:
            raise ValueError("Invalid value for `symbol_in`, must not be `None`")  # noqa: E501

        self._symbol_in = symbol_in

    @property
    def symbol_out(self) -> str:
        """Gets the symbol_out of this SwapInput.


        :return: The symbol_out of this SwapInput.
        :rtype: str
        """
        return self._symbol_out

    @symbol_out.setter
    def symbol_out(self, symbol_out: str):
        """Sets the symbol_out of this SwapInput.


        :param symbol_out: The symbol_out of this SwapInput.
        :type symbol_out: str
        """
        if symbol_out is None:
            raise ValueError("Invalid value for `symbol_out`, must not be `None`")  # noqa: E501

        self._symbol_out = symbol_out

    @property
    def amount(self) -> float:
        """Gets the amount of this SwapInput.


        :return: The amount of this SwapInput.
        :rtype: float
        """
        return self._amount

    @amount.setter
    def amount(self, amount: float):
        """Sets the amount of this SwapInput.


        :param amount: The amount of this SwapInput.
        :type amount: float
        """
        if amount is None:
            raise ValueError("Invalid value for `amount`, must not be `None`")  # noqa: E501

        self._amount = amount
