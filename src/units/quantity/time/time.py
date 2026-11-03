from __future__ import annotations

from typing import TYPE_CHECKING, Any, overload

from ...prefix import MetricPrefix
from ...types import NumericArray
from ..base import LinearQuantity
from .unit import TimeUnit

if TYPE_CHECKING:
    from ..frequency import Frequency
    from ..length import Length
    from ..speed import Speed


class Time(LinearQuantity[TimeUnit], base_unit=TimeUnit.S):
    """
    Container class for durations, which may be negative.

    The unit and its prefix are given separately: a millisecond is `TimeUnit.S` with
    `MetricPrefix.MILLI`.
    """

    @property
    def second(self) -> NumericArray:
        """Return the duration in seconds."""
        return self.base_value

    @property
    def ms(self) -> NumericArray:
        """Return the duration in milliseconds."""
        return self.in_unit(TimeUnit.S, MetricPrefix.MILLI)

    @property
    def microsecond(self) -> NumericArray:
        """Return the duration in microseconds."""
        return self.in_unit(TimeUnit.S, MetricPrefix.MICRO)

    @property
    def nanosecond(self) -> NumericArray:
        """Return the duration in nanoseconds."""
        return self.in_unit(TimeUnit.S, MetricPrefix.NANO)

    @property
    def minute(self) -> NumericArray:
        """Return the duration in minutes."""
        return self.in_unit(TimeUnit.MIN)

    @property
    def hour(self) -> NumericArray:
        """Return the duration in hours."""
        return self.in_unit(TimeUnit.HR)

    @property
    def day(self) -> NumericArray:
        """Return the duration in days."""
        return self.in_unit(TimeUnit.DAY)

    @property
    def week(self) -> NumericArray:
        """Return the duration in weeks."""
        return self.in_unit(TimeUnit.WEEK)

    @overload
    def __mul__(self, other: float | NumericArray) -> Time: ...

    @overload
    def __mul__(self, other: Speed) -> Length: ...

    @overload
    def __mul__(self, other: Frequency) -> NumericArray: ...

    @overload
    def __mul__(self, other: Any) -> Any: ...

    def __mul__(self, other: Any) -> Any:
        """
        Multiply by a speed, a frequency or a scalar.

        Parameters
        ----------
        other: Speed | Frequency | float | NumericArray
            The quantity or scalar to multiply by.

        Returns
        -------
        Length | NumericArray | Time
            The distance covered in its base unit, the number of cycles for a Frequency,
            or for a scalar, a Time in the same unit and prefix.

        Raises
        ------
        ValueError
            If the distance covered is negative.
        """
        # Imported here because these quantities refer back to Time.
        from ..frequency import Frequency
        from ..speed import Speed

        if isinstance(other, (Speed, Frequency)):
            return other * self
        return super().__mul__(other)
