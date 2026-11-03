from __future__ import annotations

import numpy as np
import pytest

from units import Mass, MassUnit, MetricPrefix

ALL_UNITS: list[tuple[MassUnit, MetricPrefix]] = [
    (MassUnit.GRAM, MetricPrefix.KILO),
    (MassUnit.GRAM, MetricPrefix.NONE),
    (MassUnit.TONNE, MetricPrefix.NONE),
    (MassUnit.POUND, MetricPrefix.NONE),
    (MassUnit.OUNCE, MetricPrefix.NONE),
    (MassUnit.CARAT, MetricPrefix.NONE),
    (MassUnit.MOMME, MetricPrefix.NONE),
    (MassUnit.KIN, MetricPrefix.NONE),
    (MassUnit.KAN, MetricPrefix.NONE),
]


def make_mass(values: list[float], unit: MassUnit, prefix: MetricPrefix = MetricPrefix.NONE) -> Mass:
    return Mass(value=np.array(values), unit=unit, prefix=prefix)


@pytest.mark.parametrize(
    ("unit", "prefix", "grams", "symbol"),
    [
        (MassUnit.GRAM, MetricPrefix.KILO, 1e3, "kg"),
        (MassUnit.GRAM, MetricPrefix.NONE, 1.0, "g"),
        (MassUnit.GRAM, MetricPrefix.MILLI, 1e-3, "mg"),
        (MassUnit.TONNE, MetricPrefix.NONE, 1e6, "t"),
        (MassUnit.TONNE, MetricPrefix.KILO, 1e9, "kt"),
        (MassUnit.POUND, MetricPrefix.NONE, 453.59237, "lb"),
        (MassUnit.OUNCE, MetricPrefix.NONE, 453.59237 / 16, "oz"),
        (MassUnit.CARAT, MetricPrefix.NONE, 0.2, "ct"),
        (MassUnit.MOMME, MetricPrefix.NONE, 3.75, "momme"),
        (MassUnit.KIN, MetricPrefix.NONE, 160 * 3.75, "kin"),
        (MassUnit.KAN, MetricPrefix.NONE, 1000 * 3.75, "kan"),
    ],
)
def test_conversion_factors_and_symbols(unit: MassUnit, prefix: MetricPrefix, grams: float, symbol: str) -> None:
    assert unit.prefixed_factor(prefix) == pytest.approx(grams)
    assert unit.symbol(prefix) == symbol


@pytest.mark.parametrize("unit", [MassUnit.POUND, MassUnit.OUNCE, MassUnit.CARAT, MassUnit.MOMME, MassUnit.KIN, MassUnit.KAN])
def test_units_outside_the_metric_system_take_no_prefix(unit: MassUnit) -> None:
    with pytest.raises(ValueError, match="no prefix"):
        _ = make_mass([1.0], unit, MetricPrefix.KILO)


@pytest.mark.parametrize("values", [[-1.0], [1.0, -0.001]])
def test_mass_rejects_negative_values(values: list[float]) -> None:
    with pytest.raises(ValueError, match="must not be negative"):
        _ = make_mass(values, MassUnit.GRAM)


def test_named_unit_properties() -> None:
    mass: Mass = make_mass([3750.0], MassUnit.GRAM)
    assert np.allclose(mass.gram, np.array([3750.0]))
    assert np.allclose(mass.kilogram, np.array([3.75]))
    assert np.allclose(mass.milligram, np.array([3.75e6]))
    assert np.allclose(mass.tonne, np.array([3.75e-3]))
    assert np.allclose(mass.pound, np.array([3750.0 / 453.59237]))
    assert np.allclose(mass.ounce, np.array([3750.0 * 16 / 453.59237]))
    assert np.allclose(mass.carat, np.array([18750.0]))
    assert np.allclose(mass.momme, np.array([1000.0]))
    assert np.allclose(mass.kin, np.array([6.25]))
    assert np.allclose(mass.kan, np.array([1.0]))


@pytest.mark.parametrize("source", ALL_UNITS)
@pytest.mark.parametrize("target", ALL_UNITS)
def test_convert_unit_all_pairs(source: tuple[MassUnit, MetricPrefix], target: tuple[MassUnit, MetricPrefix]) -> None:
    mass: Mass = make_mass([0.0, 1.0, 2.5], *source)
    expected_gram = mass.gram
    mass.convert_unit(*target)
    assert (mass.unit, mass.prefix) == target
    assert np.allclose(mass.gram, expected_gram)


def test_arithmetic() -> None:
    kilogram: Mass = make_mass([1.0], MassUnit.GRAM, MetricPrefix.KILO)
    half: Mass = make_mass([500.0], MassUnit.GRAM)
    assert (kilogram + half) == make_mass([1500.0], MassUnit.GRAM)
    assert (kilogram - half) == half
    assert (2 * half) == kilogram
    assert (half * 2) == kilogram
    assert np.allclose(np.asarray(kilogram / half), np.array([2.0]))
    halved = kilogram / 2
    assert isinstance(halved, Mass)
    assert halved.prefix is MetricPrefix.KILO
    assert halved == half


def test_string_representations() -> None:
    mass: Mass = make_mass([1.5], MassUnit.GRAM, MetricPrefix.KILO)
    assert str(mass) == "[1.5] kg"
    assert repr(mass) == "Mass(value=[1.5], unit=MassUnit.GRAM, prefix=MetricPrefix.KILO)"


def test_equality_requires_a_mass_of_the_same_shape() -> None:
    assert make_mass([1.0], MassUnit.GRAM) != make_mass([1.0, 1.0], MassUnit.GRAM)
    assert make_mass([1.0], MassUnit.GRAM) != "1 g"
