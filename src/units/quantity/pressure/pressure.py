from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

from ...prefix import MetricPrefix
from ...types import NumericArray, as_numeric_array
from ..quantity import LinearQuantity
from .unit import PressureUnit

if TYPE_CHECKING:
    from ..sound_pressure_level import SoundPressureLevel


class Pressure(LinearQuantity[PressureUnit], base_unit=PressureUnit.PASCAL):
    """
    Container class for pressures, which may be negative as a gauge pressure.

    The unit and its prefix are given separately: a hectopascal is `PressureUnit.PASCAL`
    with `MetricPrefix.HECTO`.
    """

    @property
    def pascal(self) -> NumericArray:
        """Return the pressure in pascals."""
        return self.base_value

    @property
    def hectopascal(self) -> NumericArray:
        """Return the pressure in hectopascals."""
        return self.in_unit(PressureUnit.PASCAL, MetricPrefix.HECTO)

    @property
    def kilopascal(self) -> NumericArray:
        """Return the pressure in kilopascals."""
        return self.in_unit(PressureUnit.PASCAL, MetricPrefix.KILO)

    @property
    def megapascal(self) -> NumericArray:
        """Return the pressure in megapascals."""
        return self.in_unit(PressureUnit.PASCAL, MetricPrefix.MEGA)

    @property
    def bar(self) -> NumericArray:
        """Return the pressure in bars."""
        return self.in_unit(PressureUnit.BAR)

    @property
    def millibar(self) -> NumericArray:
        """Return the pressure in millibars."""
        return self.in_unit(PressureUnit.BAR, MetricPrefix.MILLI)

    @property
    def atmosphere(self) -> NumericArray:
        """Return the pressure in standard atmospheres."""
        return self.in_unit(PressureUnit.ATMOSPHERE)

    @property
    def torr(self) -> NumericArray:
        """Return the pressure in torr."""
        return self.in_unit(PressureUnit.TORR)

    @property
    def millimeter_of_mercury(self) -> NumericArray:
        """Return the pressure in millimeters of mercury."""
        return self.in_unit(PressureUnit.MILLIMETER_OF_MERCURY)

    @property
    def kilogram_force_per_square_centimeter(self) -> NumericArray:
        """Return the pressure in kilograms-force per square centimeter."""
        return self.in_unit(PressureUnit.KILOGRAM_FORCE_PER_SQUARE_CENTIMETER)

    @property
    def pound_per_square_inch(self) -> NumericArray:
        """Return the pressure in pounds-force per square inch."""
        return self.in_unit(PressureUnit.POUND_PER_SQUARE_INCH)

    @property
    def sound_pressure_level(self) -> SoundPressureLevel:
        """
        Return the sound pressure level of this effective sound pressure in air.

        Returns
        -------
        SoundPressureLevel
            The level relative to 20 micropascals. A pressure of zero gives negative
            infinity.

        Raises
        ------
        ValueError
            If any pressure is negative, since an effective sound pressure cannot be.
        """
        # Imported here because SoundPressureLevel refers back to Pressure.
        from ..sound_pressure_level import (
            REFERENCE_SOUND_PRESSURE_PASCAL,
            SoundPressureLevel,
        )

        if np.any(self.base_value < 0):
            raise ValueError("Effective sound pressure must not be negative")
        with np.errstate(divide="ignore"):
            return SoundPressureLevel.from_base(
                as_numeric_array(
                    20.0 * np.log10(self.base_value / REFERENCE_SOUND_PRESSURE_PASCAL)
                )
            )
