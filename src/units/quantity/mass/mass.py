from __future__ import annotations

from ...prefix import MetricPrefix
from ...types import NumericArray
from ..quantity import LinearQuantity
from .unit import MassUnit


class Mass(LinearQuantity[MassUnit], base_unit=MassUnit.GRAM, is_signed=False):
    """
    Container class for masses, which cannot be negative.

    The unit and its prefix are given separately: a kilogram is `MassUnit.GRAM` with
    `MetricPrefix.KILO`.
    """

    @property
    def gram(self) -> NumericArray:
        """Return the mass in grams."""
        return self.base_value

    @property
    def kilogram(self) -> NumericArray:
        """Return the mass in kilograms."""
        return self.in_unit(MassUnit.GRAM, MetricPrefix.KILO)

    @property
    def milligram(self) -> NumericArray:
        """Return the mass in milligrams."""
        return self.in_unit(MassUnit.GRAM, MetricPrefix.MILLI)

    @property
    def tonne(self) -> NumericArray:
        """Return the mass in metric tonnes."""
        return self.in_unit(MassUnit.TONNE)

    @property
    def pound(self) -> NumericArray:
        """Return the mass in pounds."""
        return self.in_unit(MassUnit.POUND)

    @property
    def ounce(self) -> NumericArray:
        """Return the mass in ounces."""
        return self.in_unit(MassUnit.OUNCE)

    @property
    def carat(self) -> NumericArray:
        """Return the mass in carats."""
        return self.in_unit(MassUnit.CARAT)

    @property
    def momme(self) -> NumericArray:
        """Return the mass in momme."""
        return self.in_unit(MassUnit.MOMME)

    @property
    def kin(self) -> NumericArray:
        """Return the mass in kin."""
        return self.in_unit(MassUnit.KIN)

    @property
    def kan(self) -> NumericArray:
        """Return the mass in kan."""
        return self.in_unit(MassUnit.KAN)
