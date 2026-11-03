from __future__ import annotations

from typing import TYPE_CHECKING, Any, overload

from ...types import NumericArray, as_numeric_array
from ..length import Length
from ..quantity import LinearQuantity
from ..time import Time
from .unit import SpeedUnit

if TYPE_CHECKING:
    from ..frequency import Frequency


class Speed(LinearQuantity[SpeedUnit], base_unit=SpeedUnit.METER_PER_SECOND):
    """
    Container class for speeds, which may be negative as a signed velocity along an axis
    or the difference of two speeds.
    """

    @property
    def meter_per_second(self) -> NumericArray:
        """Return the speed in meters per second."""
        return self.base_value

    @property
    def kilometer_per_hour(self) -> NumericArray:
        """Return the speed in kilometers per hour."""
        return self.in_unit(SpeedUnit.KILOMETER_PER_HOUR)

    @property
    def mile_per_hour(self) -> NumericArray:
        """Return the speed in miles per hour."""
        return self.in_unit(SpeedUnit.MILE_PER_HOUR)

    @property
    def foot_per_second(self) -> NumericArray:
        """Return the speed in feet per second."""
        return self.in_unit(SpeedUnit.FOOT_PER_SECOND)

    @property
    def knot(self) -> NumericArray:
        """Return the speed in knots."""
        return self.in_unit(SpeedUnit.KNOT)

    @overload
    def __mul__(self, other: float | NumericArray) -> Speed: ...

    @overload
    def __mul__(self, other: Time) -> Length: ...

    @overload
    def __mul__(self, other: Any) -> Any: ...

    def __mul__(self, other: Any) -> Any:
        """
        Multiply by a duration or a scalar.

        Parameters
        ----------
        other: Time | float | NumericArray
            The duration or scalar to multiply by.

        Returns
        -------
        Length | Speed
            The distance covered in its base unit, or for a scalar, a Speed in the same unit.

        Raises
        ------
        ValueError
            If the distance covered is negative.
        """
        if isinstance(other, Time):
            return Length.from_base(as_numeric_array(self.base_value * other.base_value))
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: float | NumericArray) -> Speed: ...

    @overload
    def __truediv__(self, other: Speed) -> NumericArray: ...

    @overload
    def __truediv__(self, other: Frequency) -> Length: ...

    @overload
    def __truediv__(self, other: Length) -> Frequency: ...

    @overload
    def __truediv__(self, other: Any) -> Any: ...

    def __truediv__(self, other: Any) -> Any:
        """
        Divide by a speed, a frequency, a length or a scalar.

        Parameters
        ----------
        other: Speed | Frequency | Length | float | NumericArray
            The quantity or scalar to divide by.

        Returns
        -------
        NumericArray | Length | Frequency | Speed
            A ratio for a Speed, the wavelength for a Frequency, the frequency for a
            Length, or for a scalar, a Speed in the same unit.

        Raises
        ------
        ValueError
            If the speed is negative when dividing by a Frequency or a Length, since a
            wavelength or a frequency cannot be.
        """
        # Imported here because Frequency refers back to Speed.
        from ..frequency import Frequency

        if isinstance(other, Frequency):
            return Length.from_base(as_numeric_array(self.base_value / other.base_value))
        if isinstance(other, Length):
            return Frequency.from_base(as_numeric_array(self.base_value / other.base_value))
        return super().__truediv__(other)
