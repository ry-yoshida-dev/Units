from __future__ import annotations

from typing import Any, overload

from ...prefix import MetricPrefix
from ...types import NumericArray, as_numeric_array
from ..area import Area
from ..length import Length
from ..quantity import LinearQuantity
from .unit import VolumeUnit


class Volume(LinearQuantity[VolumeUnit], base_unit=VolumeUnit.CUBIC_METER, is_signed=False):
    """
    Container class for volumes, which cannot be negative.

    The unit and its prefix are given separately: a milliliter is `VolumeUnit.LITER` with
    `MetricPrefix.MILLI`.
    """

    @property
    def cubic_meter(self) -> NumericArray:
        """Return the volume in cubic meters."""
        return self.base_value

    @property
    def cubic_centimeter(self) -> NumericArray:
        """Return the volume in cubic centimeters."""
        return self.in_unit(VolumeUnit.CUBIC_METER, MetricPrefix.CENTI)

    @property
    def liter(self) -> NumericArray:
        """Return the volume in liters."""
        return self.in_unit(VolumeUnit.LITER)

    @property
    def milliliter(self) -> NumericArray:
        """Return the volume in milliliters."""
        return self.in_unit(VolumeUnit.LITER, MetricPrefix.MILLI)

    @property
    def cubic_foot(self) -> NumericArray:
        """Return the volume in cubic feet."""
        return self.in_unit(VolumeUnit.CUBIC_FOOT)

    @property
    def us_gallon(self) -> NumericArray:
        """Return the volume in US gallons."""
        return self.in_unit(VolumeUnit.US_GALLON)

    @property
    def imperial_gallon(self) -> NumericArray:
        """Return the volume in imperial gallons."""
        return self.in_unit(VolumeUnit.IMPERIAL_GALLON)

    @property
    def go(self) -> NumericArray:
        """Return the volume in go."""
        return self.in_unit(VolumeUnit.GO)

    @property
    def sho(self) -> NumericArray:
        """Return the volume in sho."""
        return self.in_unit(VolumeUnit.SHO)

    @overload
    def __truediv__(self, other: float | NumericArray) -> Volume: ...

    @overload
    def __truediv__(self, other: Volume) -> NumericArray: ...

    @overload
    def __truediv__(self, other: Area) -> Length: ...

    @overload
    def __truediv__(self, other: Length) -> Area: ...

    @overload
    def __truediv__(self, other: Any) -> Any: ...

    def __truediv__(self, other: Any) -> Any:
        """
        Divide by a volume, an area, a length or a scalar.

        Parameters
        ----------
        other: Volume | Area | Length | float | NumericArray
            The quantity or scalar to divide by.

        Returns
        -------
        NumericArray | Length | Area | Volume
            A ratio for a Volume, a Length or an Area in its base unit, or for a scalar, a
            Volume in the same unit and prefix.
        """
        if isinstance(other, Area):
            return Length.from_base(as_numeric_array(self.base_value / other.base_value))
        if isinstance(other, Length):
            return Area.from_base(as_numeric_array(self.base_value / other.base_value))
        return super().__truediv__(other)
