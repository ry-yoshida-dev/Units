from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..prefix import MetricPrefix
from ..types import NumericArray, as_numeric_array
from .unit import AreaUnit


@dataclass
class Area:
    """
    Container class for areas.

    The unit and its prefix are given separately: a square kilometer is
    `AreaUnit.SQUARE_METER` with `MetricPrefix.KILO`, and a hectare is
    `AreaUnit.ARE` with `MetricPrefix.HECTO`.

    Parameters
    ----------
    value: NumericArray
        The value of the area.
    unit: AreaUnit
        The unit of the area.
    prefix: MetricPrefix
        The prefix of the unit, or `MetricPrefix.NONE` for the unit itself.

    Raises
    ------
    ValueError
        If any value is negative, or a prefix is given to a unit that takes none.
    """

    value: NumericArray
    unit: AreaUnit
    prefix: MetricPrefix = MetricPrefix.NONE

    def __post_init__(self) -> None:
        if np.any(self.value < 0):
            raise ValueError("Area value must be positive")
        self.unit.validate_prefix(self.prefix)

    @property
    def square_meter(self) -> NumericArray:
        """
        Return the area in square meters.

        Returns
        -------
        NumericArray:
            The area in square meters.
        """
        return as_numeric_array(self.value * self.unit.prefixed_to_square_meter(self.prefix))

    @property
    def square_kilometer(self) -> NumericArray:
        """
        Return the area in square kilometers.

        Returns
        -------
        NumericArray:
            The area in square kilometers.
        """
        return self._in(AreaUnit.SQUARE_METER, MetricPrefix.KILO)

    @property
    def hectare(self) -> NumericArray:
        """
        Return the area in hectares.

        Returns
        -------
        NumericArray:
            The area in hectares.
        """
        return self._in(AreaUnit.ARE, MetricPrefix.HECTO)

    @property
    def are(self) -> NumericArray:
        """
        Return the area in ares.

        Returns
        -------
        NumericArray:
            The area in ares.
        """
        return self._in(AreaUnit.ARE, MetricPrefix.NONE)

    @property
    def tsubo(self) -> NumericArray:
        """
        Return the area in tsubo.

        Returns
        -------
        NumericArray:
            The area in tsubo.
        """
        return self._in(AreaUnit.TSUBO, MetricPrefix.NONE)

    def convert_unit(
        self,
        converted_unit: AreaUnit = AreaUnit.SQUARE_METER,
        converted_prefix: MetricPrefix = MetricPrefix.NONE,
    ) -> None:
        """
        Convert the area unit and prefix.

        Parameters
        ----------
        converted_unit: AreaUnit
            The unit to convert the area to.
        converted_prefix: MetricPrefix
            The prefix of that unit, or `MetricPrefix.NONE` for the unit itself.

        Raises
        ------
        ValueError
            If a prefix is given to a unit that takes none.
        """
        self.value = self._in(converted_unit, converted_prefix)
        self.unit = converted_unit
        self.prefix = converted_prefix

    def __add__(self, other: Area) -> Area:
        """
        Add two areas.

        Returns
        -------
        Area:
            The sum of the two areas in square meters.
        """
        return Area(value=self.square_meter + other.square_meter, unit=AreaUnit.SQUARE_METER)

    def __sub__(self, other: Area) -> Area:
        """
        Subtract two areas.

        Returns
        -------
        Area:
            The difference of the two areas in square meters.
        """
        return Area(value=self.square_meter - other.square_meter, unit=AreaUnit.SQUARE_METER)

    def __mul__(self, scalar: float | NumericArray) -> Area:
        """
        Multiply area by a scalar.

        Parameters
        ----------
        scalar: float | NumericArray
            The scalar to multiply by.

        Returns
        -------
        Area:
            The multiplied area in the same unit and prefix.
        """
        return Area(value=self.value * scalar, unit=self.unit, prefix=self.prefix)

    def __rmul__(self, scalar: float | NumericArray) -> Area:
        """
        Multiply area by a scalar (right multiplication).

        Parameters
        ----------
        scalar: float | NumericArray
            The scalar to multiply by.

        Returns
        -------
        Area:
            The multiplied area in the same unit and prefix.
        """
        return self.__mul__(scalar)

    def __truediv__(self, other: Area | float | NumericArray) -> Area | NumericArray:
        """
        Divide area by another area or a scalar.

        Parameters
        ----------
        other: Area | float | NumericArray
            The area or scalar to divide by.

        Returns
        -------
        Area | NumericArray:
            If dividing by Area, returns a NumericArray (ratio).
            If dividing by float or NumericArray, returns an Area.
        """
        if isinstance(other, Area):
            return as_numeric_array(self.square_meter / other.square_meter)
        return Area(value=as_numeric_array(self.value / other), unit=self.unit, prefix=self.prefix)

    def __eq__(self, other: object) -> bool:
        """Compare if this area is equal to another."""
        if not isinstance(other, Area):
            return False
        return self.value.shape == other.value.shape and bool(
            np.allclose(self.square_meter, other.square_meter, atol=1e-9)
        )

    def __str__(self) -> str:
        """String representation of the area."""
        return f"{self.value} {self.unit.symbol(self.prefix)}"

    def __repr__(self) -> str:
        """String representation of the area."""
        return f"Area(value={self.value}, unit={self.unit}, prefix={self.prefix})"

    def _in(self, unit: AreaUnit, prefix: MetricPrefix) -> NumericArray:
        return as_numeric_array(self.square_meter / unit.prefixed_to_square_meter(prefix))
