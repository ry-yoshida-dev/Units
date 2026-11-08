from __future__ import annotations

from typing import TYPE_CHECKING, Self, overload

from typing_extensions import override

from ...prefix import MetricPrefix
from ...types import NumericArray, as_numeric_array
from ..quantity import LinearQuantity
from .unit import LengthUnit

if TYPE_CHECKING:
    from ..area import Area
    from ..frequency import Frequency
    from ..speed import Speed
    from ..time import Time
    from ..volume import Volume


class Length(LinearQuantity[LengthUnit], base_unit=LengthUnit.M, is_signed=False):
    """
    Container class for lengths, which cannot be negative.

    The unit and its prefix are given separately: a kilometer is `LengthUnit.M` with
    `MetricPrefix.KILO`.
    """

    @property
    def meter(self) -> NumericArray:
        """Return the length in meters."""
        return self.base_value

    @property
    def km(self) -> NumericArray:
        """Return the length in kilometers."""
        return self.in_unit(LengthUnit.M, MetricPrefix.KILO)

    @property
    def cm(self) -> NumericArray:
        """Return the length in centimeters."""
        return self.in_unit(LengthUnit.M, MetricPrefix.CENTI)

    @property
    def mm(self) -> NumericArray:
        """Return the length in millimeters."""
        return self.in_unit(LengthUnit.M, MetricPrefix.MILLI)

    @property
    def micrometer(self) -> NumericArray:
        """Return the length in micrometers."""
        return self.in_unit(LengthUnit.M, MetricPrefix.MICRO)

    @property
    def nanometer(self) -> NumericArray:
        """Return the length in nanometers."""
        return self.in_unit(LengthUnit.M, MetricPrefix.NANO)

    @property
    def inch(self) -> NumericArray:
        """Return the length in inches."""
        return self.in_unit(LengthUnit.INCH)

    @property
    def foot(self) -> NumericArray:
        """Return the length in feet."""
        return self.in_unit(LengthUnit.FOOT)

    @property
    def yard(self) -> NumericArray:
        """Return the length in yards."""
        return self.in_unit(LengthUnit.YARD)

    @property
    def mile(self) -> NumericArray:
        """Return the length in miles."""
        return self.in_unit(LengthUnit.MILE)

    @property
    def nautical_mile(self) -> NumericArray:
        """Return the length in nautical miles."""
        return self.in_unit(LengthUnit.NAUTICAL_MILE)

    @property
    def sun(self) -> NumericArray:
        """Return the length in sun."""
        return self.in_unit(LengthUnit.SUN)

    @property
    def shaku(self) -> NumericArray:
        """Return the length in shaku."""
        return self.in_unit(LengthUnit.SHAKU)

    @property
    def ken(self) -> NumericArray:
        """Return the length in ken."""
        return self.in_unit(LengthUnit.KEN)

    @property
    def ri(self) -> NumericArray:
        """Return the length in ri."""
        return self.in_unit(LengthUnit.RI)

    # mypy forbids operator overrides that widen the operand types, which the
    # products and quotients with other quantities must do.
    @overload  # type: ignore[override]
    def __mul__(self, other: float | NumericArray) -> Self: ...

    @overload
    def __mul__(self, other: Length) -> Area: ...

    @overload
    def __mul__(self, other: Area) -> Volume: ...

    @overload
    def __mul__(self, other: Frequency) -> Speed: ...

    @override
    def __mul__(
        self, other: float | NumericArray | Length | Area | Frequency
    ) -> Self | Area | Volume | Speed:
        """
        Multiply by a length, an area, a frequency or a scalar.

        Parameters
        ----------
        other: Length | Area | Frequency | float | NumericArray
            The quantity or scalar to multiply by.

        Returns
        -------
        Area | Volume | Speed | Length
            An Area, a Volume or a Speed in its base unit, or for a scalar, a Length in
            the same unit and prefix.
        """
        # Imported here because these quantities refer back to Length.
        from ..area import Area
        from ..frequency import Frequency
        from ..speed import Speed
        from ..volume import Volume

        if isinstance(other, Length):
            return Area.from_base(as_numeric_array(self.base_value * other.base_value))
        if isinstance(other, Area):
            return Volume.from_base(
                as_numeric_array(self.base_value * other.base_value)
            )
        if isinstance(other, Frequency):
            return Speed.from_base(as_numeric_array(self.base_value * other.base_value))
        return super().__mul__(other)

    # mypy forbids operator overrides that widen the operand types, which the
    # products and quotients with other quantities must do.
    @overload  # type: ignore[override]
    def __truediv__(self, other: LinearQuantity[LengthUnit]) -> NumericArray: ...

    @overload
    def __truediv__(self, other: float | NumericArray) -> Self: ...

    @overload
    def __truediv__(self, other: Time) -> Speed: ...

    @overload
    def __truediv__(self, other: Speed) -> Time: ...

    @override
    def __truediv__(
        self, other: LinearQuantity[LengthUnit] | float | NumericArray | Time | Speed
    ) -> NumericArray | Self | Speed | Time:
        """
        Divide by a length, a duration, a speed or a scalar.

        Parameters
        ----------
        other: Length | Time | Speed | float | NumericArray
            The quantity or scalar to divide by.

        Returns
        -------
        NumericArray | Speed | Time | Length
            A ratio for a Length, a Speed or a Time in its base unit, or for a scalar, a
            Length in the same unit and prefix.
        """
        # Imported here because these quantities refer back to Length.
        from ..speed import Speed
        from ..time import Time

        if isinstance(other, Time):
            return Speed.from_base(as_numeric_array(self.base_value / other.base_value))
        if isinstance(other, Speed):
            return Time.from_base(as_numeric_array(self.base_value / other.base_value))
        return super().__truediv__(other)
