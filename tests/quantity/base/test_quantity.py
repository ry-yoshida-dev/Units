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
