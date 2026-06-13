from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..types import NumericArray

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

    def __post_init__(self):
        if self.value.ndim != 1:
            raise ValueError("Angle must be a 1D array")

    @property
    def radian(self) -> NumericArray:
        """
        Return the angle in radians.

        Returns
        -------
        NumericArray:
            The angle in radians.
        """
        match self.unit:
            case AngleUnit.DEGREE:
                return np.deg2rad(self.value)
            case AngleUnit.RADIAN:
                return self.value

    @property
    def degree(self) -> NumericArray:
        """
        Return the angle in degrees.

        Returns
        -------
        NumericArray:
            The angle in degrees.
        """
        match self.unit:
            case AngleUnit.DEGREE:
                return self.value
            case AngleUnit.RADIAN:
                return np.rad2deg(self.value)

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

        Parameters:
        ----------
        converted_unit: AngleUnit
            The unit to convert the angle to.
        """
        if self.unit == converted_unit:
            return
        match converted_unit:
            case AngleUnit.DEGREE:
                new_value = self.degree
            case AngleUnit.RADIAN:
                new_value = self.radian
        self.value = new_value
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

    def __len__(self) -> int:
        """
        Return the length of the angle.
        
        Returns
        -------
        int:
            The length of the angle.
        """
        return len(self.value)

