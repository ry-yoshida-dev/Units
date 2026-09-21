from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..types import NumericArray, as_numeric_array

from .degrees_minutes_seconds import DegreesMinutesSeconds
from .unit import AngleUnit

@dataclass
class Angle:
    """
    Container class for angles.

    Parameters
    ----------
    value: NumericArray
        The value array of the angle.
    unit: AngleUnit
        The unit of the angle.
    """
    value: NumericArray
    unit: AngleUnit

    def __post_init__(self) -> None:
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
        signed_seconds: NumericArray = self._value_in(AngleUnit.ARCSECOND)
        return DegreesMinutesSeconds.normalized(
            degrees=as_numeric_array(np.zeros_like(signed_seconds)),
            minutes=as_numeric_array(np.zeros_like(signed_seconds)),
            seconds=as_numeric_array(np.abs(signed_seconds)),
            is_negative=signed_seconds < 0,
            )

    @property
    def radian(self) -> NumericArray:
        """
        Return the angle in radians.

        Returns
        -------
        NumericArray:
            The angle in radians.
        """
        return self._value_in(AngleUnit.RADIAN)

    @property
    def degree(self) -> NumericArray:
        """
        Return the angle in degrees.

        Returns
        -------
        NumericArray:
            The angle in degrees.
        """
        return self.value * self.unit.to_degree

    def _value_in(self, target_unit: AngleUnit) -> NumericArray:
        if self.unit == target_unit:
            return self.value
        return as_numeric_array(self.degree / target_unit.to_degree)

    @property
    def is_degree(self) -> bool:
        """
        Return True if the angle is in degree.
        """
        return self.unit.is_degree
    
    @property
    def is_radian(self) -> bool:
        """
        Return True if the angle is in radian.
        """
        return self.unit.is_radian

    def convert_unit(
        self, 
        converted_unit: AngleUnit= AngleUnit.DEGREE
        ) -> None:
        """
        Convert the angle unit.

        Parameters
        ----------
        converted_unit: AngleUnit
            The unit to convert the angle to.
        """
        self.value = self._value_in(converted_unit)
        self.unit = converted_unit

    @property
    def sin(self) -> NumericArray:
        """
        Return the sine of the angle.

        Returns
        -------
        NumericArray:
            The sine of the angle.
        """
        return np.sin(self.radian)
    
    @property
    def cos(self) -> NumericArray:
        """
        Return the cosine of the angle.

        Returns
        -------
        NumericArray:
            The cosine of the angle.
        """
        return np.cos(self.radian)
    
    @property
    def tan(self) -> NumericArray:
        """
        Return the tangent of the angle.

        Returns
        -------
        NumericArray:
            The tangent of the angle.
        """
        return np.tan(self.radian)
    
    def __add__(
        self, 
        other: Angle
        ) -> Angle:
        """
        Add two angles.

        Returns
        -------
        Angle:
            The sum of the two angles.
        """
        return Angle(
            value=self.radian + other.radian, 
            unit=AngleUnit.RADIAN
            )
    
    def __sub__(
        self, 
        other: Angle
        ) -> Angle:
        """
        Subtract two angles.
        
        Returns
        -------
        Angle:
            The difference of the two angles.
        """
        return Angle(
            value=self.radian - other.radian, 
            unit=AngleUnit.RADIAN
            )

    def __neg__(self) -> Angle:
        """
        Negate the angle.

        Returns
        -------
        Angle:
            The negated angle in the same unit.
        """
        return Angle(
            value=as_numeric_array(-self.value),
            unit=self.unit
            )

    def __eq__(self, other: object) -> bool:
        """Compare if this angle is equal to another."""
        if not isinstance(other, Angle):
            return False
        return self.value.shape == other.value.shape and np.allclose(self.degree, other.degree, atol=1e-9)

    def __len__(self) -> int:
        """
        Return the length of the angle.
        
        Returns
        -------
        int:
            The length of the angle.
        """
        return len(self.value)

