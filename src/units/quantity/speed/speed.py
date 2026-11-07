from __future__ import annotations

from typing import TYPE_CHECKING, overload

from typing_extensions import Self, override

from ...types import NumericArray, as_numeric_array
from ..length import Length
from ..quantity import LinearQuantity
from ..time import Time
from .unit import SpeedUnit

if TYPE_CHECKING:
    from ..frequency import Frequency


class Speed(LinearQuantity[SpeedUnit], base_unit=SpeedUnit.METER_PER_SECOND):
    """
    Container class for speeds, which may be negative.

    A negative speed is a signed velocity along an axis or the difference of two speeds.
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

    # mypy forbids operator overrides that widen the operand types, which the
    # products and quotients with other quantities must do.
    @overload  # type: ignore[override]
    def __mul__(self, other: float | NumericArray) -> Self: ...

    @overload
    def __mul__(self, other: Time) -> Length: ...

    @override
    def __mul__(self, other: float | NumericArray | Time) -> Self | Length:
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
            return Length.from_base(
                as_numeric_array(self.base_value * other.base_value)
            )
        return super().__mul__(other)

    # mypy forbids operator overrides that widen the operand types, which the
    # products and quotients with other quantities must do.
    @overload  # type: ignore[override]
    def __truediv__(self, other: LinearQuantity[SpeedUnit]) -> NumericArray: ...

    @overload
    def __truediv__(self, other: float | NumericArray) -> Self: ...

    @overload
    def __truediv__(self, other: Frequency) -> Length: ...

    @overload
    def __truediv__(self, other: Length) -> Frequency: ...

    @override
    def __truediv__(
        self,
        other: LinearQuantity[SpeedUnit] | float | NumericArray | Frequency | Length,
    ) -> NumericArray | Self | Length | Frequency:
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
            return Length.from_base(
                as_numeric_array(self.base_value / other.base_value)
            )
        if isinstance(other, Length):
            return Frequency.from_base(
                as_numeric_array(self.base_value / other.base_value)
            )
        return super().__truediv__(other)
