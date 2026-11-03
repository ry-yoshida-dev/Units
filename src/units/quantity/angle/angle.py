from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from ...types import NumericArray, as_numeric_array
from ..quantity import LinearQuantity
from .degrees_minutes_seconds import DegreesMinutesSeconds
from .unit import AngleUnit

if TYPE_CHECKING:
    from typing_extensions import Self


class Angle(LinearQuantity[AngleUnit], base_unit=AngleUnit.DEGREE):
    """
    Container class for one-dimensional arrays of angles, which may be negative.

    Sums and differences are returned in radians.
    """

    def __post_init__(self) -> None:
        super().__post_init__()
        if self.value.ndim != 1:
            raise ValueError("Angle must be a 1D array")

    @classmethod
    def from_degrees_minutes_seconds(
        cls,
        sexagesimal: DegreesMinutesSeconds,
        ) -> Angle:
        """
        Build an angle from sexagesimal degrees, minutes and seconds.

        Parameters
        ----------
        sexagesimal : DegreesMinutesSeconds
            The signed angle in degrees, minutes and seconds.

        Returns
        -------
        Angle
            The angle in degrees.
        """
        angle: Angle = cls(value=sexagesimal.total_seconds, unit=AngleUnit.ARCSECOND)
        angle.convert_unit(AngleUnit.DEGREE)
        return angle

    @property
    def degrees_minutes_seconds(self) -> DegreesMinutesSeconds:
        """
        Return the angle in sexagesimal degrees, minutes and seconds.

        Returns
        -------
        DegreesMinutesSeconds
            The signed angle in canonical degrees, minutes and seconds.
        """
        signed_seconds: NumericArray = self.in_unit(AngleUnit.ARCSECOND)
        return DegreesMinutesSeconds.normalized(
            degrees=as_numeric_array(np.zeros_like(signed_seconds)),
            minutes=as_numeric_array(np.zeros_like(signed_seconds)),
            seconds=as_numeric_array(np.abs(signed_seconds)),
            is_negative=signed_seconds < 0,
            )

    @property
    def degree(self) -> NumericArray:
        """Return the angle in degrees."""
        return self.base_value

    @property
    def radian(self) -> NumericArray:
        """Return the angle in radians."""
        return self.in_unit(AngleUnit.RADIAN)

    @property
    def gradian(self) -> NumericArray:
        """Return the angle in gradians."""
        return self.in_unit(AngleUnit.GRADIAN)

    @property
    def turn(self) -> NumericArray:
        """Return the angle in turns."""
        return self.in_unit(AngleUnit.TURN)

    @property
    def is_degree(self) -> bool:
        """Return True if the angle is in degree."""
        return self.unit.is_degree

    @property
    def is_radian(self) -> bool:
        """Return True if the angle is in radian."""
        return self.unit.is_radian

    @property
    def sin(self) -> NumericArray:
        """Return the sine of the angle."""
        return np.sin(self.radian)

    @property
    def cos(self) -> NumericArray:
        """Return the cosine of the angle."""
        return np.cos(self.radian)

    @property
    def tan(self) -> NumericArray:
        """Return the tangent of the angle."""
        return np.tan(self.radian)

    def __add__(self, other: LinearQuantity[AngleUnit]) -> Self:
        """
        Add two angles.

        Returns
        -------
        Self
            The sum of the two angles in radians.
        """
        if not isinstance(other, Angle):
            return NotImplemented
        return type(self)(value=as_numeric_array(self.radian + other.radian), unit=AngleUnit.RADIAN)

    def __sub__(self, other: LinearQuantity[AngleUnit]) -> Self:
        """
        Subtract two angles.

        Returns
        -------
        Self
            The difference of the two angles in radians.
        """
        if not isinstance(other, Angle):
            return NotImplemented
        return type(self)(value=as_numeric_array(self.radian - other.radian), unit=AngleUnit.RADIAN)

    def __len__(self) -> int:
        """Return the number of angles."""
        return len(self.value)
