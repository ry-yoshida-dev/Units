from __future__ import annotations

from typing import Any, overload

from ...prefix import MetricPrefix
from ...types import NumericArray, as_numeric_array
from ..length import Length
from ..quantity import LinearQuantity
from ..speed import Speed
from ..time import Time
from .unit import FrequencyUnit


class Frequency(LinearQuantity[FrequencyUnit], base_unit=FrequencyUnit.HERTZ, is_signed=False):
    """
    Container class for frequencies, which cannot be negative.

    The unit and its prefix are given separately: a kilohertz is `FrequencyUnit.HERTZ`
    with `MetricPrefix.KILO`.
    """

    @property
    def hertz(self) -> NumericArray:
        """Return the frequency in hertz."""
        return self.base_value

    @property
    def kilohertz(self) -> NumericArray:
        """Return the frequency in kilohertz."""
        return self.in_unit(FrequencyUnit.HERTZ, MetricPrefix.KILO)

    @property
    def megahertz(self) -> NumericArray:
        """Return the frequency in megahertz."""
        return self.in_unit(FrequencyUnit.HERTZ, MetricPrefix.MEGA)

    @property
    def gigahertz(self) -> NumericArray:
        """Return the frequency in gigahertz."""
        return self.in_unit(FrequencyUnit.HERTZ, MetricPrefix.GIGA)

    @property
    def rpm(self) -> NumericArray:
        """Return the frequency in revolutions per minute."""
        return self.in_unit(FrequencyUnit.RPM)

    @property
    def bpm(self) -> NumericArray:
        """Return the frequency in beats per minute."""
        return self.in_unit(FrequencyUnit.BPM)

    @property
    def period(self) -> Time:
        """Return the duration of one cycle in seconds."""
        return Time.from_base(as_numeric_array(1.0 / self.base_value))

    @overload
    def __mul__(self, other: float | NumericArray) -> Frequency: ...

    @overload
    def __mul__(self, other: Time) -> NumericArray: ...

    @overload
    def __mul__(self, other: Length) -> Speed: ...

    @overload
    def __mul__(self, other: Any) -> Any: ...

    def __mul__(self, other: Any) -> Any:
        """
        Multiply by a duration, a length or a scalar.

        Parameters
        ----------
        other: Time | Length | float | NumericArray
            The quantity or scalar to multiply by.

        Returns
        -------
        NumericArray | Speed | Frequency
            The number of cycles for a Time, the speed of a wave of that wavelength for a
            Length, or for a scalar, a Frequency in the same unit and prefix.
        """
        if isinstance(other, Time):
            return as_numeric_array(self.base_value * other.base_value)
        if isinstance(other, Length):
            return Speed.from_base(as_numeric_array(self.base_value * other.base_value))
        return super().__mul__(other)
