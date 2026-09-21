from __future__ import annotations

import itertools

import numpy as np
import pytest

from units import Length, LengthUnit, NumericArray

ALL_LENGTH_UNITS: list[LengthUnit] = list(LengthUnit)

METERS_PER_UNIT: dict[LengthUnit, float] = {
    LengthUnit.KM: 1000.0,
    LengthUnit.M: 1.0,
    LengthUnit.CM: 0.01,
    LengthUnit.MM: 0.001,
    LengthUnit.INCH: 0.0254,
}


def make_length(values: list[float], unit: LengthUnit) -> Length:
    return Length(value=np.array(values), unit=unit)


@pytest.mark.parametrize("unit", ALL_LENGTH_UNITS)
def test_unit_to_meter(unit: LengthUnit) -> None:
    assert unit.to_meter == pytest.approx(METERS_PER_UNIT[unit])


@pytest.mark.parametrize("values", [[-1.0], [1.0, -0.001]])
def test_length_rejects_negative_values(values: list[float]) -> None:
    with pytest.raises(ValueError, match="positive"):
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


def test_convert_unit_defaults_to_meter() -> None:
    length: Length = make_length([2.0], LengthUnit.KM)
    length.convert_unit()
    assert length.unit == LengthUnit.M
    assert np.allclose(length.value, np.array([2000.0]))


def test_convert_unit_to_same_unit_keeps_value() -> None:
    value: NumericArray = np.array([3.0])
    length: Length = Length(value=value, unit=LengthUnit.CM)
    length.convert_unit(LengthUnit.CM)
    assert length.value is value


def test_addition_mixes_units_and_returns_meter() -> None:
    total: Length = make_length([1.0], LengthUnit.M) + make_length([100.0], LengthUnit.CM)
    assert total.unit == LengthUnit.M
    assert np.allclose(total.value, np.array([2.0]))


def test_subtraction_mixes_units_and_returns_meter() -> None:
    difference: Length = make_length([1.0], LengthUnit.KM) - make_length([250.0], LengthUnit.M)
    assert difference.unit == LengthUnit.M
    assert np.allclose(difference.value, np.array([750.0]))


def test_subtraction_rejects_negative_result() -> None:
    with pytest.raises(ValueError, match="positive"):
        _ = make_length([1.0], LengthUnit.M) - make_length([2.0], LengthUnit.M)


def test_multiplication_by_scalar_keeps_unit() -> None:
    length: Length = make_length([1.5], LengthUnit.KM)
    for product in [length * 2.0, 2.0 * length]:
        assert product.unit == LengthUnit.KM
        assert np.allclose(product.value, np.array([3.0]))


def test_multiplication_by_array_is_elementwise() -> None:
    product: Length = make_length([1.0, 2.0], LengthUnit.M) * np.array([3.0, 4.0])
    assert np.allclose(product.value, np.array([3.0, 8.0]))


def test_multiplication_by_negative_scalar_is_rejected() -> None:
    with pytest.raises(ValueError, match="positive"):
        _ = make_length([1.0], LengthUnit.M) * -1.0


def test_division_by_length_returns_ratio() -> None:
    ratio: Length | NumericArray = make_length([1.0], LengthUnit.M) / make_length([50.0], LengthUnit.CM)
    assert isinstance(ratio, np.ndarray)
    assert np.allclose(ratio, np.array([2.0]))


def test_division_by_scalar_keeps_unit() -> None:
    quotient: Length | NumericArray = make_length([3.0], LengthUnit.KM) / 2.0
    assert isinstance(quotient, Length)
    assert quotient.unit == LengthUnit.KM
    assert np.allclose(quotient.value, np.array([1.5]))


def test_division_by_array_is_elementwise() -> None:
    quotient: Length | NumericArray = make_length([4.0, 9.0], LengthUnit.M) / np.array([2.0, 3.0])
    assert isinstance(quotient, Length)
    assert np.allclose(quotient.value, np.array([2.0, 3.0]))


def test_equality_across_units() -> None:
    assert make_length([1.0], LengthUnit.KM) == make_length([1000.0], LengthUnit.M)
    assert make_length([1.0], LengthUnit.INCH) == make_length([25.4], LengthUnit.MM)


def test_inequality_on_different_values() -> None:
    assert make_length([1.0], LengthUnit.M) != make_length([1.1], LengthUnit.M)


def test_inequality_on_different_shapes() -> None:
    assert make_length([1.0], LengthUnit.M) != make_length([1.0, 1.0, 1.0], LengthUnit.M)


def test_inequality_with_other_types() -> None:
    assert make_length([1.0], LengthUnit.M) != 1.0


def test_string_representations() -> None:
    length: Length = make_length([2.0], LengthUnit.KM)
    assert str(length) == "[2.] km"
    assert repr(length) == "Length(value=[2.], unit=LengthUnit.KM)"
