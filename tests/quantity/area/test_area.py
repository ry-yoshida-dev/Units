from __future__ import annotations

import numpy as np
import pytest

from units import Area, AreaUnit, MetricPrefix

PREFIXED_UNITS: list[tuple[AreaUnit, MetricPrefix]] = [
    (AreaUnit.SQUARE_METER, MetricPrefix.KILO),
    (AreaUnit.SQUARE_METER, MetricPrefix.NONE),
    (AreaUnit.SQUARE_METER, MetricPrefix.CENTI),
    (AreaUnit.ARE, MetricPrefix.HECTO),
    (AreaUnit.ARE, MetricPrefix.NONE),
    (AreaUnit.SQUARE_FOOT, MetricPrefix.NONE),
    (AreaUnit.ACRE, MetricPrefix.NONE),
    (AreaUnit.TSUBO, MetricPrefix.NONE),
    (AreaUnit.JO, MetricPrefix.NONE),
    (AreaUnit.SE, MetricPrefix.NONE),
    (AreaUnit.TAN, MetricPrefix.NONE),
    (AreaUnit.CHO, MetricPrefix.NONE),
]


def make_area(values: list[float], unit: AreaUnit, prefix: MetricPrefix = MetricPrefix.NONE) -> Area:
    return Area(value=np.array(values), unit=unit, prefix=prefix)


@pytest.mark.parametrize(
    ("unit", "prefix", "square_meters", "symbol"),
    [
        (AreaUnit.SQUARE_METER, MetricPrefix.KILO, 1e6, "km2"),
        (AreaUnit.SQUARE_METER, MetricPrefix.NONE, 1.0, "m2"),
        (AreaUnit.SQUARE_METER, MetricPrefix.MILLI, 1e-6, "mm2"),
        (AreaUnit.ARE, MetricPrefix.HECTO, 1e4, "ha"),
        (AreaUnit.ARE, MetricPrefix.NONE, 100.0, "a"),
        (AreaUnit.SQUARE_FOOT, MetricPrefix.NONE, 0.3048**2, "ft2"),
        (AreaUnit.ACRE, MetricPrefix.NONE, 43560 * 0.3048**2, "acre"),
        (AreaUnit.TSUBO, MetricPrefix.NONE, 400 / 121, "tsubo"),
        (AreaUnit.JO, MetricPrefix.NONE, 1.62, "jo"),
        (AreaUnit.SE, MetricPrefix.NONE, 30 * 400 / 121, "se"),
        (AreaUnit.TAN, MetricPrefix.NONE, 300 * 400 / 121, "tan"),
        (AreaUnit.CHO, MetricPrefix.NONE, 3000 * 400 / 121, "cho"),
    ],
)
def test_prefix_is_raised_to_the_power_of_the_unit(
    unit: AreaUnit, prefix: MetricPrefix, square_meters: float, symbol: str
) -> None:
    assert unit.prefixed_factor(prefix) == pytest.approx(square_meters)
    assert unit.symbol(prefix) == symbol


def test_tsubo_takes_no_prefix() -> None:
    with pytest.raises(ValueError, match="no prefix"):
        _ = make_area([1.0], AreaUnit.TSUBO, MetricPrefix.KILO)
    assert make_area([1.0], AreaUnit.TSUBO).prefix is MetricPrefix.NONE


def test_prefix_is_applied_without_compounding_float_error() -> None:
    assert AreaUnit.SQUARE_METER.prefixed_factor(MetricPrefix.DECI) == 10.0**-2


@pytest.mark.parametrize("values", [[-1.0], [1.0, -0.001]])
def test_area_rejects_negative_values(values: list[float]) -> None:
    with pytest.raises(ValueError, match="must not be negative"):
        _ = make_area(values, AreaUnit.SQUARE_METER)


def test_named_unit_properties() -> None:
    area: Area = make_area([25_000.0], AreaUnit.SQUARE_METER)
    assert np.allclose(area.square_kilometer, np.array([0.025]))
    assert np.allclose(area.hectare, np.array([2.5]))
    assert np.allclose(area.are, np.array([250.0]))
    assert np.allclose(area.tsubo, np.array([25_000.0 * 121 / 400]))
    assert np.allclose(area.square_foot, np.array([25_000.0 / 0.3048**2]))
    assert np.allclose(area.acre, np.array([25_000.0 / (43560 * 0.3048**2)]))
    assert np.allclose(area.jo, np.array([25_000.0 / 1.62]))
    assert np.allclose(area.se, np.array([25_000.0 * 121 / 12_000]))
    assert np.allclose(area.tan, np.array([25_000.0 * 121 / 120_000]))
    assert np.allclose(area.cho, np.array([25_000.0 * 121 / 1_200_000]))


@pytest.mark.parametrize("source", PREFIXED_UNITS)
@pytest.mark.parametrize("target", PREFIXED_UNITS)
def test_convert_unit_all_pairs(
    source: tuple[AreaUnit, MetricPrefix], target: tuple[AreaUnit, MetricPrefix]
) -> None:
    area: Area = make_area([0.0, 1.0, 2.5], *source)
    expected_square_meter = area.square_meter
    area.convert_unit(*target)
    assert (area.unit, area.prefix) == target
    assert np.allclose(area.square_meter, expected_square_meter)


def test_convert_unit_rejects_a_prefix_the_unit_does_not_take() -> None:
    area: Area = make_area([1.0], AreaUnit.SQUARE_METER)
    with pytest.raises(ValueError, match="no prefix"):
        area.convert_unit(AreaUnit.TSUBO, MetricPrefix.KILO)


def test_arithmetic() -> None:
    hectare: Area = make_area([1.0], AreaUnit.ARE, MetricPrefix.HECTO)
    are: Area = make_area([50.0], AreaUnit.ARE)
    assert (hectare + are) == make_area([15_000.0], AreaUnit.SQUARE_METER)
    assert (hectare - are) == make_area([5_000.0], AreaUnit.SQUARE_METER)
    assert (2 * are) == hectare
    assert np.allclose(np.asarray(hectare / are), np.array([2.0]))
    halved = hectare / 2
    assert isinstance(halved, Area)
    assert halved.prefix is MetricPrefix.HECTO
    assert halved == make_area([50.0], AreaUnit.ARE)


def test_string_shows_the_prefixed_symbol() -> None:
    assert str(make_area([1.5], AreaUnit.ARE, MetricPrefix.HECTO)) == "[1.5] ha"


def test_equality_requires_an_area_of_the_same_shape() -> None:
    assert make_area([1.0], AreaUnit.ARE) != make_area([1.0, 1.0], AreaUnit.ARE)
    assert make_area([1.0], AreaUnit.ARE) != "1 a"
