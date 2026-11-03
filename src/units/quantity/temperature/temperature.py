from __future__ import annotations

import numpy as np

from ...types import NumericArray, as_numeric_array
from ..base import Quantity
from .unit import TemperatureUnit


class Temperature(Quantity[TemperatureUnit], base_unit=TemperatureUnit.KELVIN):
    """
    Container class for absolute temperatures, which cannot be below absolute zero.

    A temperature has no sum or scalar product, since their result would depend on the
    unit. Subtracting two temperatures returns their difference in kelvin instead.
    """

    def __post_init__(self) -> None:
        super().__post_init__()
        if np.any(self.base_value < 0):
            raise ValueError("Temperature must not be below absolute zero")

    @property
    def kelvin(self) -> NumericArray:
        """Return the temperature in kelvin."""
        return self.base_value

    @property
    def celsius(self) -> NumericArray:
        """Return the temperature in degrees Celsius."""
        return self.in_unit(TemperatureUnit.CELSIUS)

    @property
    def fahrenheit(self) -> NumericArray:
        """Return the temperature in degrees Fahrenheit."""
        return self.in_unit(TemperatureUnit.FAHRENHEIT)

    @property
    def rankine(self) -> NumericArray:
        """Return the temperature in degrees Rankine."""
        return self.in_unit(TemperatureUnit.RANKINE)

    def __sub__(self, other: Temperature) -> NumericArray:
        """
        Subtract two temperatures.

        Returns
        -------
        NumericArray
            The difference of the two temperatures in kelvin.
        """
        if not isinstance(other, Temperature):
            return NotImplemented
        return as_numeric_array(self.base_value - other.base_value)
