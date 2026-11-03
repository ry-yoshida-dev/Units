from __future__ import annotations

import itertools

import numpy as np
import pytest

from units import Length, LengthUnit, MetricPrefix, NumericArray

ALL_LENGTH_UNITS: list[LengthUnit] = list(LengthUnit)

METERS_PER_UNIT: dict[LengthUnit, float] = {
    LengthUnit.M: 1.0,
    LengthUnit.INCH: 0.0254,
    LengthUnit.FOOT: 0.3048,
    LengthUnit.YARD: 0.9144,
    LengthUnit.MILE: 1609.344,
    LengthUnit.NAUTICAL_MILE: 1852.0,
    LengthUnit.SUN: 1.0 / 33.0,
    LengthUnit.SHAKU: 10.0 / 33.0,
    LengthUnit.KEN: 20.0 / 11.0,
    LengthUnit.RI: 43200.0 / 11.0,
}


def make_length(values: list[float], unit: LengthUnit, prefix: MetricPrefix = MetricPrefix.NONE) -> Length:
    return Length(value=np.array(values), unit=unit, prefix=prefix)


@pytest.mark.parametrize(
    ("prefix", "meters", "symbol"),
    [
        (MetricPrefix.KILO, 1000.0, "km"),
        (MetricPrefix.NONE, 1.0, "m"),
        (MetricPrefix.CENTI, 0.01, "cm"),
        (MetricPrefix.MILLI, 0.001, "mm"),
        (MetricPrefix.MICRO, 1e-6, "µm"),
        (MetricPrefix.NANO, 1e-9, "nm"),
    ],
)
def test_prefix_scales_the_meter(prefix: MetricPrefix, meters: float, symbol: str) -> None:
    assert LengthUnit.M.prefixed_factor(prefix) == pytest.approx(meters)
    assert LengthUnit.M.symbol(prefix) == symbol


@pytest.mark.parametrize("unit", [unit for unit in LengthUnit if unit is not LengthUnit.M])
def test_only_the_meter_takes_a_prefix(unit: LengthUnit) -> None:
    with pytest.raises(ValueError, match="no prefix"):
        _ = make_length([1.0], unit, MetricPrefix.KILO)


def test_one_tsubo_is_a_square_of_one_ken() -> None:
    assert LengthUnit.KEN.factor**2 == pytest.approx(400 / 121)


@pytest.mark.parametrize("unit", ALL_LENGTH_UNITS)
def test_unit_to_meter(unit: LengthUnit) -> None:
    assert unit.factor == pytest.approx(METERS_PER_UNIT[unit])


@pytest.mark.parametrize("values", [[-1.0], [1.0, -0.001]])
def test_length_rejects_negative_values(values: list[float]) -> None:
    with pytest.raises(ValueError, match="must not be negative"):
        _ = make_length(values, LengthUnit.M)


def test_length_accepts_zero() -> None:
    assert np.allclose(make_length([0.0], LengthUnit.M).meter, np.array([0.0]))


@pytest.mark.parametrize("unit", ALL_LENGTH_UNITS)
def test_meter_property(unit: LengthUnit) -> None:
    length: Length = make_length([2.0, 3.0], unit)
    assert np.allclose(length.meter, np.array([2.0, 3.0]) * METERS_PER_UNIT[unit])


def test_named_unit_properties() -> None:
    length: Length = make_length([2.54], LengthUnit.M)
    assert np.allclose(length.km, np.array([0.00254]))
    assert np.allclose(length.cm, np.array([254.0]))
    assert np.allclose(length.mm, np.array([2540.0]))
    assert np.allclose(length.inch, np.array([100.0]))
    assert np.allclose(length.micrometer, np.array([2.54e6]))
    assert np.allclose(length.nanometer, np.array([2.54e9]))
    assert np.allclose(length.foot, np.array([2.54 / 0.3048]))
    assert np.allclose(length.yard, np.array([2.54 / 0.9144]))
    assert np.allclose(length.mile, np.array([2.54 / 1609.344]))
    assert np.allclose(length.nautical_mile, np.array([2.54 / 1852.0]))
    assert np.allclose(length.sun, np.array([2.54 * 33.0]))
    assert np.allclose(length.shaku, np.array([2.54 * 3.3]))
    assert np.allclose(length.ken, np.array([2.54 * 0.55]))
    assert np.allclose(length.ri, np.array([2.54 * 11.0 / 43200.0]))


@pytest.mark.parametrize(
    ("source_unit", "target_unit"),
    list(itertools.product(ALL_LENGTH_UNITS, ALL_LENGTH_UNITS)),
)
def test_convert_unit_all_pairs(source_unit: LengthUnit, target_unit: LengthUnit) -> None:
    length: Length = make_length([0.0, 1.0, 2.5], source_unit)
    expected_meter: NumericArray = length.meter
    length.convert_unit(target_unit)
    assert length.unit == target_unit
    assert np.allclose(length.meter, expected_meter)
    assert np.allclose(length.value, expected_meter / METERS_PER_UNIT[target_unit])


def test_convert_unit_changes_the_prefix() -> None:
    length: Length = make_length([2.0], LengthUnit.M, MetricPrefix.KILO)
    length.convert_unit(LengthUnit.M, MetricPrefix.CENTI)
    assert length.prefix is MetricPrefix.CENTI
    assert np.allclose(length.value, np.array([200000.0]))


def test_convert_unit_rejects_a_prefix_the_unit_does_not_take() -> None:
    with pytest.raises(ValueError, match="no prefix"):
        make_length([1.0], LengthUnit.M).convert_unit(LengthUnit.INCH, MetricPrefix.KILO)


def test_convert_unit_defaults_to_meter() -> None:
    length: Length = make_length([2.0], LengthUnit.M, MetricPrefix.KILO)
    length.convert_unit()
    assert length.unit == LengthUnit.M
    assert np.allclose(length.value, np.array([2000.0]))


def test_convert_unit_to_same_unit_keeps_value() -> None:
    value: NumericArray = np.array([3.0])
    length: Length = Length(value=value, unit=LengthUnit.M, prefix=MetricPrefix.CENTI)
    length.convert_unit(LengthUnit.M, MetricPrefix.CENTI)
    assert length.value is value


def test_addition_mixes_units_and_returns_meter() -> None:
    total: Length = make_length([1.0], LengthUnit.M) + make_length([100.0], LengthUnit.M, MetricPrefix.CENTI)
    assert total.unit == LengthUnit.M
    assert np.allclose(total.value, np.array([2.0]))


def test_subtraction_mixes_units_and_returns_meter() -> None:
    difference: Length = make_length([1.0], LengthUnit.M, MetricPrefix.KILO) - make_length([250.0], LengthUnit.M)
    assert difference.unit == LengthUnit.M
    assert np.allclose(difference.value, np.array([750.0]))


def test_subtraction_rejects_negative_result() -> None:
    with pytest.raises(ValueError, match="must not be negative"):
        _ = make_length([1.0], LengthUnit.M) - make_length([2.0], LengthUnit.M)


def test_multiplication_by_scalar_keeps_unit() -> None:
    length: Length = make_length([1.5], LengthUnit.M, MetricPrefix.KILO)
    for product in [length * 2.0, 2.0 * length]:
        assert product.unit == LengthUnit.M
        assert product.prefix is MetricPrefix.KILO
        assert np.allclose(product.value, np.array([3.0]))


def test_multiplication_by_array_is_elementwise() -> None:
    product: Length = make_length([1.0, 2.0], LengthUnit.M) * np.array([3.0, 4.0])
    assert np.allclose(product.value, np.array([3.0, 8.0]))


def test_multiplication_by_negative_scalar_is_rejected() -> None:
    with pytest.raises(ValueError, match="must not be negative"):
        _ = make_length([1.0], LengthUnit.M) * -1.0


def test_division_by_length_returns_ratio() -> None:
    ratio: Length | NumericArray = make_length([1.0], LengthUnit.M) / make_length([50.0], LengthUnit.M, MetricPrefix.CENTI)
    assert isinstance(ratio, np.ndarray)
    assert np.allclose(ratio, np.array([2.0]))


def test_division_by_scalar_keeps_unit() -> None:
    quotient: Length | NumericArray = make_length([3.0], LengthUnit.M, MetricPrefix.KILO) / 2.0
    assert isinstance(quotient, Length)
    assert quotient.unit == LengthUnit.M
    assert quotient.prefix is MetricPrefix.KILO
    assert np.allclose(quotient.value, np.array([1.5]))


def test_division_by_array_is_elementwise() -> None:
    quotient: Length | NumericArray = make_length([4.0, 9.0], LengthUnit.M) / np.array([2.0, 3.0])
    assert isinstance(quotient, Length)
    assert np.allclose(quotient.value, np.array([2.0, 3.0]))


def test_equality_across_units() -> None:
    assert make_length([1.0], LengthUnit.M, MetricPrefix.KILO) == make_length([1000.0], LengthUnit.M)
    assert make_length([1.0], LengthUnit.INCH) == make_length([25.4], LengthUnit.M, MetricPrefix.MILLI)


def test_inequality_on_different_values() -> None:
    assert make_length([1.0], LengthUnit.M) != make_length([1.1], LengthUnit.M)


def test_inequality_on_different_shapes() -> None:
    assert make_length([1.0], LengthUnit.M) != make_length([1.0, 1.0, 1.0], LengthUnit.M)


def test_inequality_with_other_types() -> None:
    assert make_length([1.0], LengthUnit.M) != 1.0


def test_string_representations() -> None:
    length: Length = make_length([2.0], LengthUnit.M, MetricPrefix.KILO)
    assert str(length) == "[2.] km"
    assert repr(length) == "Length(value=[2.], unit=LengthUnit.M, prefix=MetricPrefix.KILO)"
