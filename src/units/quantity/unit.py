from enum import Enum

import numpy as np

from ..prefix import MetricPrefix
from ..types import NumericArray, as_numeric_array


class Unit(Enum):
    """
    Base enum for units, without any prefix.

    A unit takes no prefix unless it overrides `is_prefixable`. Subclasses define how a
    value converts to and from the base unit of their quantity.
    """

    @property
    def is_prefixable(self) -> bool:
        """
        Return whether this unit takes an SI prefix.

        Returns
        -------
        bool
            False for units outside the metric system, such as the tsubo.
        """
        return False

    @property
    def prefix_power(self) -> int:
        """
        Return the power a prefix is raised to when scaling this unit.

        Returns
        -------
        int
            2 for the square meter, whose prefix scales its side, and 1 for a unit
            whose prefix scales the unit itself.
        """
        return 1

    def validate_prefix(self, prefix: MetricPrefix) -> None:
        """
        Check that this unit takes a prefix.

        Parameters
        ----------
        prefix: MetricPrefix
            The prefix, or `MetricPrefix.NONE` for the unit itself.

        Raises
        ------
        ValueError
            If a prefix other than `MetricPrefix.NONE` is given to a unit that takes none.
        """
        if prefix is not MetricPrefix.NONE and not self.is_prefixable:
            raise ValueError(f"{self.value} takes no prefix: {prefix.value}")

    def symbol(self, prefix: MetricPrefix = MetricPrefix.NONE) -> str:
        """
        Return the symbol of this unit with a prefix.

        Parameters
        ----------
        prefix: MetricPrefix
            The prefix, or `MetricPrefix.NONE` for the unit itself.

        Returns
        -------
        str
            The symbol, such as `km2` or `ha`.
        """
        return f"{prefix.value}{self.value}"

    def scale(self, prefix: MetricPrefix = MetricPrefix.NONE) -> float:
        """
        Return the size of one step of this unit in the base unit of the quantity.

        Parameters
        ----------
        prefix: MetricPrefix
            The prefix, or `MetricPrefix.NONE` for the unit itself.

        Returns
        -------
        float
            The size of one step, ignoring any offset between the scales.
        """
        return float(self.to_base(np.array(1.0), prefix) - self.to_base(np.array(0.0), prefix))

    def to_base(self, value: NumericArray, prefix: MetricPrefix = MetricPrefix.NONE) -> NumericArray:
        """
        Convert values in this unit to the base unit of the quantity.

        Parameters
        ----------
        value: NumericArray
            The values in this unit.
        prefix: MetricPrefix
            The prefix, or `MetricPrefix.NONE` for the unit itself.

        Returns
        -------
        NumericArray
            The values in the base unit.
        """
        raise NotImplementedError

    def from_base(self, value: NumericArray, prefix: MetricPrefix = MetricPrefix.NONE) -> NumericArray:
        """
        Convert values in the base unit of the quantity to this unit.

        Parameters
        ----------
        value: NumericArray
            The values in the base unit.
        prefix: MetricPrefix
            The prefix, or `MetricPrefix.NONE` for the unit itself.

        Returns
        -------
        NumericArray
            The values in this unit.
        """
        raise NotImplementedError


class LinearUnit(Unit):
    """
    Base enum for units that differ from the base unit only by a factor.
    """

    @property
    def factor(self) -> float:
        """
        Return the number of base units in one of this unit, without a prefix.

        Returns
        -------
        float
            The conversion factor to the base unit.
        """
        raise NotImplementedError

    def prefixed_factor(self, prefix: MetricPrefix = MetricPrefix.NONE) -> float:
        """
        Return the number of base units in one of this unit with a prefix.

        Parameters
        ----------
        prefix: MetricPrefix
            The prefix, or `MetricPrefix.NONE` for the unit itself.

        Returns
        -------
        float
            Ten to the prefix exponent times `prefix_power`, times `factor`.

        Raises
        ------
        ValueError
            If a prefix other than `MetricPrefix.NONE` is given to a unit that takes none.
        """
        self.validate_prefix(prefix)
        return 10.0 ** (prefix.exponent * self.prefix_power) * self.factor

    def to_base(self, value: NumericArray, prefix: MetricPrefix = MetricPrefix.NONE) -> NumericArray:
        return as_numeric_array(value * self.prefixed_factor(prefix))

    def from_base(self, value: NumericArray, prefix: MetricPrefix = MetricPrefix.NONE) -> NumericArray:
        return as_numeric_array(value / self.prefixed_factor(prefix))
