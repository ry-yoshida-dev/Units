from __future__ import annotations

from typing import TYPE_CHECKING, Any, overload

from ...prefix import MetricPrefix
from ...types import NumericArray, as_numeric_array
from ..quantity import LinearQuantity
from .unit import AreaUnit

if TYPE_CHECKING:
    from ..length import Length
    from ..volume import Volume


class Area(LinearQuantity[AreaUnit], base_unit=AreaUnit.SQUARE_METER, is_signed=False):
    """
    Container class for areas, which cannot be negative.

    The unit and its prefix are given separately: a square kilometer is
    `AreaUnit.SQUARE_METER` with `MetricPrefix.KILO`, and a hectare is
    `AreaUnit.ARE` with `MetricPrefix.HECTO`.
    """

    @property
    def square_meter(self) -> NumericArray:
        """Return the area in square meters."""
        return self.base_value

    @property
    def square_kilometer(self) -> NumericArray:
        """Return the area in square kilometers."""
        return self.in_unit(AreaUnit.SQUARE_METER, MetricPrefix.KILO)

    @property
    def hectare(self) -> NumericArray:
        """Return the area in hectares."""
        return self.in_unit(AreaUnit.ARE, MetricPrefix.HECTO)

    @property
    def are(self) -> NumericArray:
        """Return the area in ares."""
        return self.in_unit(AreaUnit.ARE)

    @property
    def square_foot(self) -> NumericArray:
        """Return the area in square feet."""
        return self.in_unit(AreaUnit.SQUARE_FOOT)

    @property
    def acre(self) -> NumericArray:
        """Return the area in acres."""
        return self.in_unit(AreaUnit.ACRE)

    @property
    def tsubo(self) -> NumericArray:
        """Return the area in tsubo."""
        return self.in_unit(AreaUnit.TSUBO)

    @property
    def jo(self) -> NumericArray:
        """Return the area in jo."""
        return self.in_unit(AreaUnit.JO)

    @property
    def se(self) -> NumericArray:
        """Return the area in se."""
        return self.in_unit(AreaUnit.SE)

    @property
    def tan(self) -> NumericArray:
        """Return the area in tan."""
        return self.in_unit(AreaUnit.TAN)

    @property
    def cho(self) -> NumericArray:
        """Return the area in cho."""
        return self.in_unit(AreaUnit.CHO)

    @overload
    def __mul__(self, other: float | NumericArray) -> Area: ...

    @overload
    def __mul__(self, other: Length) -> Volume: ...

    @overload
    def __mul__(self, other: Any) -> Any: ...

    def __mul__(self, other: Any) -> Any:
        """
        Multiply by a length or a scalar.

        Parameters
        ----------
        other: Length | float | NumericArray
            The length or scalar to multiply by.

        Returns
        -------
        Volume | Area
            A Volume in its base unit, or for a scalar, an Area in the same unit and prefix.
        """
        # Imported here because these quantities refer back to Area.
        from ..length import Length
        from ..volume import Volume

        if isinstance(other, Length):
            return Volume.from_base(as_numeric_array(self.base_value * other.base_value))
        return super().__mul__(other)

    @overload
    def __truediv__(self, other: float | NumericArray) -> Area: ...

    @overload
    def __truediv__(self, other: Area) -> NumericArray: ...

    @overload
    def __truediv__(self, other: Length) -> Length: ...

    @overload
    def __truediv__(self, other: Any) -> Any: ...

    def __truediv__(self, other: Any) -> Any:
        """
        Divide by an area, a length or a scalar.

        Parameters
        ----------
        other: Area | Length | float | NumericArray
            The quantity or scalar to divide by.

        Returns
        -------
        NumericArray | Length | Area
            A ratio for an Area, a Length in its base unit, or for a scalar, an Area in
            the same unit and prefix.
        """
        from ..length import Length

        if isinstance(other, Length):
            return Length.from_base(as_numeric_array(self.base_value / other.base_value))
        return super().__truediv__(other)
