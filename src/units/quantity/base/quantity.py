from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, ClassVar, Generic, TypeVar, overload

import numpy as np

from ...prefix import MetricPrefix
from ...types import NumericArray, as_numeric_array
from .unit import LinearUnit, Unit

if TYPE_CHECKING:
    from typing_extensions import Self

UnitT = TypeVar("UnitT", bound=Unit)
LinearUnitT = TypeVar("LinearUnitT", bound=LinearUnit)

EQUALITY_TOLERANCE: float = 1e-9


@dataclass
class Quantity(Generic[UnitT]):
    """
    Base container for the values of a physical quantity.

    Subclasses are declared with the unit their arithmetic results are expressed in and
    whether they accept negative values, such as
    `class Length(LinearQuantity[LengthUnit], base_unit=LengthUnit.M, is_signed=False)`.

    Parameters
    ----------
    value: NumericArray
        The values of the quantity.
    unit: UnitT
        The unit of the values.
    prefix: MetricPrefix
        The prefix of the unit, or `MetricPrefix.NONE` for the unit itself.

    Raises
    ------
    TypeError
        If the unit belongs to another quantity.
    ValueError
        If a negative value is given to an unsigned quantity, or a prefix is given to a
        unit that takes none.
    """

    value: NumericArray
    unit: UnitT
    prefix: MetricPrefix = MetricPrefix.NONE

    _base_unit: ClassVar[Any]
    _is_signed: ClassVar[bool] = True

    # Makes NumPy defer to `__rmul__` instead of multiplying element by element.
    __array_ufunc__: ClassVar[None] = None

    def __init_subclass__(cls, *, base_unit: Unit | None = None, is_signed: bool | None = None) -> None:
        super().__init_subclass__()
        if base_unit is not None:
            cls._base_unit = base_unit
        if is_signed is not None:
            cls._is_signed = is_signed

    def __post_init__(self) -> None:
        self._validate_unit(self.unit)
        if not self._is_signed and np.any(self.value < 0):
            raise ValueError(f"{type(self).__name__} value must not be negative")
        self.unit.validate_prefix(self.prefix)

    def _validate_unit(self, unit: Unit) -> None:
        unit_type: type[Unit] = type(self._base_unit)
        if not isinstance(unit, unit_type):
            raise TypeError(f"{type(self).__name__} takes a {unit_type.__name__}, given: {unit!r}")

    @classmethod
    def from_base(cls, value: NumericArray) -> Self:
        """
        Build a quantity from values in its base unit.

        Parameters
        ----------
        value: NumericArray
            The values in the base unit.

        Returns
        -------
        Self
            The quantity in its base unit.
        """
        return cls(value=value, unit=cls._base_unit)

    @property
    def base_value(self) -> NumericArray:
        """
        Return the values in the base unit.

        Returns
        -------
        NumericArray
            The values in the base unit.
        """
        return self.unit.to_base(self.value, self.prefix)

    def in_unit(self, unit: UnitT, prefix: MetricPrefix = MetricPrefix.NONE) -> NumericArray:
        """
        Return the values in a unit and prefix.

        Parameters
        ----------
        unit: UnitT
            The unit to express the values in.
        prefix: MetricPrefix
            The prefix of that unit, or `MetricPrefix.NONE` for the unit itself.

        Returns
        -------
        NumericArray
            A new array of the values in that unit and prefix.

        Raises
        ------
        TypeError
            If the unit belongs to another quantity.
        ValueError
            If a prefix is given to a unit that takes none.
        """
        self._validate_unit(unit)
        if unit == self.unit and prefix == self.prefix:
            return as_numeric_array(np.copy(self.value))
        return unit.from_base(self.base_value, prefix)

    def convert_unit(
        self,
        converted_unit: UnitT | None = None,
        converted_prefix: MetricPrefix = MetricPrefix.NONE,
    ) -> None:
        """
        Convert the unit and prefix in place.

        Parameters
        ----------
        converted_unit: UnitT | None
            The unit to convert to, or None for the base unit.
        converted_prefix: MetricPrefix
            The prefix of that unit, or `MetricPrefix.NONE` for the unit itself.

        Raises
        ------
        TypeError
            If the unit belongs to another quantity.
        ValueError
            If a prefix is given to a unit that takes none.
        """
        unit: UnitT = self._base_unit if converted_unit is None else converted_unit
        if unit == self.unit and converted_prefix == self.prefix:
            return
        self.value = self.in_unit(unit, converted_prefix)
        self.unit = unit
        self.prefix = converted_prefix

    def __eq__(self, other: object) -> bool:
        """
        Compare with another quantity of the same type in its base unit.

        The absolute tolerance follows the finer of the two units, since a fixed one in the
        base unit would make small values such as 1 nm and 2 nm equal.
        """
        if type(other) is not type(self):
            return False
        absolute_tolerance: float = EQUALITY_TOLERANCE * min(
            self.unit.scale(self.prefix), other.unit.scale(other.prefix)
        )
        return np.shape(self.value) == np.shape(other.value) and bool(
            np.allclose(self.base_value, other.base_value, rtol=EQUALITY_TOLERANCE, atol=absolute_tolerance)
        )

    def __str__(self) -> str:
        """String representation with the prefixed unit symbol."""
        return f"{self.value} {self.unit.symbol(self.prefix)}"

    def __repr__(self) -> str:
        """String representation with the unit and prefix members."""
        return f"{type(self).__name__}(value={self.value}, unit={self.unit}, prefix={self.prefix})"


class LinearQuantity(Quantity[LinearUnitT]):
    """
    Base container for quantities with sums and scalar products.

    Sums are returned in the base unit, and scalar products and quotients keep the unit
    and prefix. Dividing by the same quantity returns a plain ratio. Arithmetic with any
    other quantity raises `TypeError` unless a subclass defines it.
    """

    def __add__(self, other: Self) -> Self:
        """
        Add a quantity of the same type.

        Returns
        -------
        Self
            The sum in the base unit.
        """
        if type(other) is not type(self):
            return NotImplemented
        return self.from_base(as_numeric_array(self.base_value + other.base_value))

    def __sub__(self, other: Self) -> Self:
        """
        Subtract a quantity of the same type.

        Returns
        -------
        Self
            The difference in the base unit.
        """
        if type(other) is not type(self):
            return NotImplemented
        return self.from_base(as_numeric_array(self.base_value - other.base_value))

    def __neg__(self) -> Self:
        """
        Negate the quantity.

        Returns
        -------
        Self
            The negated quantity in the same unit and prefix.

        Raises
        ------
        TypeError
            If the quantity is unsigned.
        """
        if not self._is_signed:
            raise TypeError(f"bad operand type for unary -: '{type(self).__name__}'")
        return type(self)(value=as_numeric_array(-self.value), unit=self.unit, prefix=self.prefix)

    @overload
    def __mul__(self, other: float | NumericArray) -> Self: ...

    @overload
    def __mul__(self, other: Any) -> Any: ...

    def __mul__(self, other: Any) -> Any:
        """
        Multiply by a scalar.

        Parameters
        ----------
        other: float | NumericArray
            The scalar to multiply by.

        Returns
        -------
        Self
            The multiplied quantity in the same unit and prefix.
        """
        if isinstance(other, Quantity):
            return NotImplemented
        return type(self)(value=as_numeric_array(self.value * other), unit=self.unit, prefix=self.prefix)

    def __rmul__(self, other: float | NumericArray) -> Self:
        """
        Multiply by a scalar (right multiplication).

        Parameters
        ----------
        other: float | NumericArray
            The scalar to multiply by.

        Returns
        -------
        Self
            The multiplied quantity in the same unit and prefix.
        """
        if isinstance(other, Quantity):
            return NotImplemented
        return type(self)(value=as_numeric_array(self.value * other), unit=self.unit, prefix=self.prefix)

    @overload
    def __truediv__(self, other: float | NumericArray) -> Self: ...

    @overload
    def __truediv__(self, other: Any) -> Any: ...

    def __truediv__(self, other: Any) -> Any:
        """
        Divide by a quantity of the same type or a scalar.

        Parameters
        ----------
        other: Self | float | NumericArray
            The quantity or scalar to divide by.

        Returns
        -------
        Self | NumericArray
            If dividing by the same quantity, returns a NumericArray (ratio).
            If dividing by float or NumericArray, returns the quantity in the same unit
            and prefix.
        """
        if type(other) is type(self):
            return as_numeric_array(self.base_value / other.base_value)
        if isinstance(other, Quantity):
            return NotImplemented
        return type(self)(value=as_numeric_array(self.value / other), unit=self.unit, prefix=self.prefix)
