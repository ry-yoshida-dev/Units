from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ..types import NumericArray, as_numeric_array

from .unit import TimeUnit


@dataclass
class Time:
    """
    Container class for durations.

    Parameters
    ----------
    value: NumericArray
        The value of the duration.
    unit: TimeUnit
        The unit of the duration.
    """
    value: NumericArray
    unit: TimeUnit

    @property
    def second(self) -> NumericArray:
        """
        Return the duration in seconds.

        Returns
        -------
        NumericArray:
            The duration in seconds.
        """
        return self.value * self.unit.to_second

    @property
    def ms(self) -> NumericArray:
        """
        Return the duration in milliseconds.

        Returns
        -------
        NumericArray:
            The duration in milliseconds.
        """
        return as_numeric_array(self.second / TimeUnit.MS.to_second)

    @property
    def minute(self) -> NumericArray:
        """
        Return the duration in minutes.

        Returns
        -------
        NumericArray:
            The duration in minutes.
        """
        return as_numeric_array(self.second / TimeUnit.MIN.to_second)

    @property
    def hour(self) -> NumericArray:
        """
        Return the duration in hours.

        Returns
        -------
        NumericArray:
            The duration in hours.
        """
        return as_numeric_array(self.second / TimeUnit.HR.to_second)

    @property
    def day(self) -> NumericArray:
        """
        Return the duration in days.

        Returns
        -------
        NumericArray:
            The duration in days.
        """
        return as_numeric_array(self.second / TimeUnit.DAY.to_second)

    def convert_unit(
        self,
        converted_unit: TimeUnit = TimeUnit.S,
    ) -> None:
        """
        Convert the duration unit.

        Parameters
        ----------
        converted_unit: TimeUnit
            The unit to convert the duration to.
        """
        if self.unit == converted_unit:
            return

        sec_value = self.second
        self.value = as_numeric_array(sec_value / converted_unit.to_second)
        self.unit = converted_unit

    def __add__(self, other: Time) -> Time:
        """
        Add two durations.

        Returns
        -------
        Time:
            The sum of the two durations in seconds.
        """
        return Time(
            value=self.second + other.second,
            unit=TimeUnit.S,
        )

    def __sub__(self, other: Time) -> Time:
        """
        Subtract two durations.

        Returns
        -------
        Time:
            The difference of the two durations in seconds.
        """
        return Time(
            value=self.second - other.second,
            unit=TimeUnit.S,
        )

    def __mul__(self, scalar: float | NumericArray) -> Time:
        """
        Multiply duration by a scalar.

        Parameters
        ----------
        scalar: float | NumericArray
            The scalar to multiply by.

        Returns
        -------
        Time:
            The multiplied duration in the same unit.
        """
        return Time(
            value=self.value * scalar,
            unit=self.unit,
        )

    def __rmul__(self, scalar: float | NumericArray) -> Time:
        """
        Multiply duration by a scalar (right multiplication).

        Parameters
        ----------
        scalar: float | NumericArray
            The scalar to multiply by.

        Returns
        -------
        Time:
            The multiplied duration in the same unit.
        """
        return self.__mul__(scalar)

    def __truediv__(self, other: Time | float | NumericArray) -> Time | NumericArray:
        """
        Divide duration by another duration or a scalar.

        Parameters
        ----------
        other: Time | float | NumericArray
            The duration or scalar to divide by.

        Returns
        -------
        Time | NumericArray:
            If dividing by Time, returns a NumericArray (ratio).
            If dividing by float or NumericArray, returns a Time.
        """
        if isinstance(other, Time):
            return as_numeric_array(self.second / other.second)
        return Time(
            value=as_numeric_array(self.value / other),
            unit=self.unit,
        )

    def __eq__(self, other: object) -> bool:
        """Compare if this duration is equal to another."""
        if not isinstance(other, Time):
            return False
        return np.allclose(self.second, other.second, atol=1e-9)

    def __str__(self) -> str:
        """String representation of the duration."""
        return f"{self.value} {self.unit.value}"

    def __repr__(self) -> str:
        """String representation of the duration."""
        return f"Time(value={self.value}, unit={self.unit})"
