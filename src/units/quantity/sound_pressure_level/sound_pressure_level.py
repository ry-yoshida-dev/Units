from __future__ import annotations

import numpy as np

from ...types import NumericArray, as_numeric_array
from ..base import Quantity
from ..pressure import Pressure
from .unit import SoundPressureLevelUnit

REFERENCE_SOUND_PRESSURE_PASCAL = 20e-6


class SoundPressureLevel(Quantity[SoundPressureLevelUnit], base_unit=SoundPressureLevelUnit.DECIBEL):
    """
    Container class for sound pressure levels in air, relative to 20 micropascals.

    A level is logarithmic and may be negative. Adding levels combines uncorrelated
    sources by their energy, so two sources of 60 dB make about 63 dB, and subtracting
    returns the difference in decibels. A level has no scalar product. Weighted levels
    such as dB(A) depend on the spectrum and cannot be converted from this value.
    """

    @property
    def decibel(self) -> NumericArray:
        """Return the level in decibels."""
        return self.base_value

    @property
    def bel(self) -> NumericArray:
        """Return the level in bels."""
        return self.in_unit(SoundPressureLevelUnit.BEL)

    @property
    def pressure(self) -> Pressure:
        """Return the effective sound pressure in pascals."""
        return Pressure.from_base(as_numeric_array(REFERENCE_SOUND_PRESSURE_PASCAL * 10.0 ** (self.base_value / 20.0)))

    def __add__(self, other: SoundPressureLevel) -> SoundPressureLevel:
        """
        Combine with the level of an uncorrelated source by energy.

        Returns
        -------
        SoundPressureLevel
            The combined level in decibels.
        """
        if not isinstance(other, SoundPressureLevel):
            return NotImplemented
        energy = 10.0 ** (self.base_value / 10.0) + 10.0 ** (other.base_value / 10.0)
        return self.from_base(as_numeric_array(10.0 * np.log10(energy)))

    def __sub__(self, other: SoundPressureLevel) -> NumericArray:
        """
        Subtract another level.

        Returns
        -------
        NumericArray
            The difference of the two levels in decibels.
        """
        if not isinstance(other, SoundPressureLevel):
            return NotImplemented
        return as_numeric_array(self.base_value - other.base_value)
