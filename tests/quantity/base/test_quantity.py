from __future__ import annotations

from typing import Any

import numpy as np
import pytest

import units
from units.quantity.base import LinearQuantity, Quantity, Unit


def all_subclasses(cls: type) -> list[type]:
    return [cls for sub in cls.__subclasses__() for cls in [sub, *all_subclasses(sub)]]


QUANTITIES: list[type[Any]] = [cls for cls in all_subclasses(Quantity) if hasattr(cls, "_base_unit")]
LINEAR_QUANTITIES: list[type[Any]] = [cls for cls in QUANTITIES if issubclass(cls, LinearQuantity)]


def unit_enum(quantity: type[Any]) -> type[Unit]:
    return type(quantity._base_unit)


def test_every_quantity_and_its_unit_are_exported() -> None:
    assert len(QUANTITIES) >= 11
    for quantity in QUANTITIES:
        assert getattr(units, quantity.__name__) is quantity
        assert getattr(units, unit_enum(quantity).__name__) is unit_enum(quantity)


@pytest.mark.parametrize("quantity", QUANTITIES, ids=lambda cls: cls.__name__)
def test_every_unit_round_trips_through_the_base_unit(quantity: type[Any]) -> None:
    for unit in unit_enum(quantity):
        value = quantity(value=np.array([300.0, 500.0]), unit=unit)
        restored = quantity.from_base(value.base_value)
        restored.convert_unit(unit)
        assert restored.unit is unit
        assert np.allclose(restored.value, value.value)


@pytest.mark.parametrize("quantity", QUANTITIES, ids=lambda cls: cls.__name__)
def test_convert_unit_defaults_to_the_base_unit(quantity: type[Any]) -> None:
    for unit in unit_enum(quantity):
        value = quantity(value=np.array([300.0]), unit=unit)
        value.convert_unit()
        assert value.unit is quantity._base_unit
        assert value == quantity(value=np.array([300.0]), unit=unit)


@pytest.mark.parametrize("quantity", LINEAR_QUANTITIES, ids=lambda cls: cls.__name__)
def test_the_base_unit_of_a_linear_quantity_has_a_factor_of_one(quantity: type[Any]) -> None:
    assert quantity._base_unit.factor == 1


@pytest.mark.parametrize("quantity", LINEAR_QUANTITIES, ids=lambda cls: cls.__name__)
def test_scalar_arithmetic_keeps_the_unit(quantity: type[Any]) -> None:
    for unit in unit_enum(quantity):
        value = quantity(value=np.array([2.0]), unit=unit)
        for result in [value * 2.0, 2.0 * value, value / 2.0]:
            assert type(result) is quantity
            assert result.unit is unit
        assert np.allclose(value / value, np.array([1.0]))


@pytest.mark.parametrize("quantity", QUANTITIES, ids=lambda cls: cls.__name__)
def test_every_unit_has_a_symbol(quantity: type[Any]) -> None:
    for unit in unit_enum(quantity):
        assert isinstance(unit.symbol(), str) and unit.symbol()


@pytest.mark.parametrize("quantity", QUANTITIES, ids=lambda cls: cls.__name__)
def test_a_unit_of_another_quantity_is_rejected(quantity: type[Any]) -> None:
    other_unit = units.MassUnit.GRAM if quantity is not units.Mass else units.LengthUnit.M
    with pytest.raises(TypeError, match="takes a"):
        quantity(value=np.array([1.0]), unit=other_unit)
    value = quantity(value=np.array([1.0]), unit=quantity._base_unit)
    with pytest.raises(TypeError, match="takes a"):
        value.in_unit(other_unit)
    with pytest.raises(TypeError, match="takes a"):
        value.convert_unit(other_unit)
    assert value.unit is quantity._base_unit


@pytest.mark.parametrize(
    ("small", "other"),
    [
        (units.Length(np.array([1.0]), units.LengthUnit.M, units.MetricPrefix.NANO), units.Length(np.array([2.0]), units.LengthUnit.M, units.MetricPrefix.NANO)),
        (units.Length(np.array([1.0]), units.LengthUnit.M, units.MetricPrefix.NANO), units.Length(np.array([0.0]), units.LengthUnit.M)),
        (units.Time(np.array([1.0]), units.TimeUnit.S, units.MetricPrefix.NANO), units.Time(np.array([1.5]), units.TimeUnit.S, units.MetricPrefix.NANO)),
        (units.Volume(np.array([1.0]), units.VolumeUnit.CUBIC_METER, units.MetricPrefix.MILLI), units.Volume(np.array([2.0]), units.VolumeUnit.CUBIC_METER, units.MetricPrefix.MILLI)),
        (units.Area(np.array([1.0]), units.AreaUnit.SQUARE_METER, units.MetricPrefix.MICRO), units.Area(np.array([900.0]), units.AreaUnit.SQUARE_METER, units.MetricPrefix.MICRO)),
        (units.Mass(np.array([1.0]), units.MassUnit.GRAM, units.MetricPrefix.NANO), units.Mass(np.array([2.0]), units.MassUnit.GRAM, units.MetricPrefix.NANO)),
        (units.Length(np.array([100000.0]), units.LengthUnit.M), units.Length(np.array([100000.5]), units.LengthUnit.M)),
    ],
)
def test_equality_tells_apart_different_values_at_any_scale(small: Any, other: Any) -> None:
    assert small != other


def test_equality_ignores_floating_point_noise_across_units() -> None:
    assert units.Length(np.array([1.0]), units.LengthUnit.M, units.MetricPrefix.NANO) == units.Length(
        np.array([1e-9]), units.LengthUnit.M
    )
    assert units.Length(np.array([0.1 + 0.2]), units.LengthUnit.M) == units.Length(np.array([0.3]), units.LengthUnit.M)


def test_equality_does_not_fail_on_a_scalar_value() -> None:
    assert units.Length(1.0, units.LengthUnit.M) == units.Length(1.0, units.LengthUnit.M)  # type: ignore[arg-type]


@pytest.mark.parametrize("quantity", QUANTITIES, ids=lambda cls: cls.__name__)
def test_in_unit_never_shares_memory_with_the_quantity(quantity: type[Any]) -> None:
    value = quantity(value=np.array([1.0]), unit=quantity._base_unit)
    result = value.in_unit(quantity._base_unit)
    result[0] = 99.0
    assert value.value[0] == 1.0


@pytest.mark.parametrize("quantity", LINEAR_QUANTITIES, ids=lambda cls: cls.__name__)
def test_an_array_times_a_quantity_is_a_quantity(quantity: type[Any]) -> None:
    value = quantity(value=np.array([1.0, 2.0]), unit=quantity._base_unit)
    result = np.array([2.0, 3.0]) * value
    assert type(result) is quantity
    assert np.allclose(result.value, np.array([2.0, 6.0]))


def test_an_array_divided_by_a_quantity_is_rejected() -> None:
    with pytest.raises(TypeError):
        np.array([1.0]) / units.Time(np.array([2.0]), units.TimeUnit.S)


@pytest.mark.parametrize("quantity", LINEAR_QUANTITIES, ids=lambda cls: cls.__name__)
def test_negation_is_defined_only_for_signed_quantities(quantity: type[Any]) -> None:
    value = quantity(value=np.array([0.0]), unit=quantity._base_unit)
    if quantity._is_signed:
        assert type(-value) is quantity
    else:
        with pytest.raises(TypeError, match="unary"):
            _ = -value


def test_a_subclass_inherits_whether_it_is_signed() -> None:
    class Height(units.Length):
        pass

    with pytest.raises(ValueError, match="must not be negative"):
        Height(np.array([-1.0]), units.LengthUnit.M)


def test_equality_allows_noise_around_zero_in_the_scale_of_the_unit() -> None:
    assert units.Length(np.array([abs(0.3 - 0.1 - 0.2)]), units.LengthUnit.M) == units.Length(np.array([0.0]), units.LengthUnit.M)


@pytest.mark.parametrize(
    ("unit", "expected"),
    [
        (units.TemperatureUnit.CELSIUS, 1.0),
        (units.TemperatureUnit.FAHRENHEIT, 5.0 / 9.0),
        (units.LengthUnit.FOOT, 0.3048),
    ],
)
def test_scale_ignores_the_offset_of_the_unit(unit: Unit, expected: float) -> None:
    assert unit.scale() == pytest.approx(expected)


def test_scale_includes_the_prefix() -> None:
    assert units.AreaUnit.SQUARE_METER.scale(units.MetricPrefix.KILO) == pytest.approx(1e6)
