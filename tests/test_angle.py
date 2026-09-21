from __future__ import annotations

import itertools
import math

import numpy as np
import pytest

from units import Angle, AngleUnit, DegreesMinutesSeconds, NumericArray

ALL_ANGLE_UNITS: list[AngleUnit] = list(AngleUnit)

DEGREES_PER_UNIT: dict[AngleUnit, float] = {
    AngleUnit.DEGREE: 1.0,
    AngleUnit.ARCMINUTE: 1.0 / 60.0,
    AngleUnit.ARCSECOND: 1.0 / 3600.0,
    AngleUnit.RADIAN: 180.0 / math.pi,
}


def make_angle(values: list[float], unit: AngleUnit) -> Angle:
    return Angle(value=np.array(values), unit=unit)


@pytest.mark.parametrize("unit", ALL_ANGLE_UNITS)
def test_unit_to_degree(unit: AngleUnit) -> None:
    assert unit.to_degree == pytest.approx(DEGREES_PER_UNIT[unit])


@pytest.mark.parametrize(
    ("unit", "expected_upper", "expected_lower"),
    [
        (AngleUnit.DEGREE, "DEGREE", "degree"),
        (AngleUnit.ARCMINUTE, "ARCMINUTE", "arcminute"),
        (AngleUnit.ARCSECOND, "ARCSECOND", "arcsecond"),
        (AngleUnit.RADIAN, "RADIAN", "radian"),
    ],
)
def test_unit_case_names(unit: AngleUnit, expected_upper: str, expected_lower: str) -> None:
    assert unit.as_upper == expected_upper
    assert unit.as_lower == expected_lower


@pytest.mark.parametrize(
    ("unit", "is_degree", "is_radian"),
    [
        (AngleUnit.DEGREE, True, False),
        (AngleUnit.ARCMINUTE, False, False),
        (AngleUnit.ARCSECOND, False, False),
        (AngleUnit.RADIAN, False, True),
    ],
)
def test_unit_and_angle_flags(unit: AngleUnit, is_degree: bool, is_radian: bool) -> None:
    angle: Angle = make_angle([1.0], unit)
    assert unit.is_degree is is_degree
    assert unit.is_radian is is_radian
    assert angle.is_degree is is_degree
    assert angle.is_radian is is_radian


@pytest.mark.parametrize("shape", [(), (1, 1), (2, 3)])
def test_angle_requires_1d(shape: tuple[int, ...]) -> None:
    with pytest.raises(ValueError, match="1D"):
        _ = Angle(value=np.zeros(shape), unit=AngleUnit.DEGREE)


def test_angle_accepts_empty_array() -> None:
    angle: Angle = make_angle([], AngleUnit.DEGREE)
    assert len(angle) == 0


@pytest.mark.parametrize(
    ("unit", "value", "expected_degree"),
    [
        (AngleUnit.DEGREE, 180.0, 180.0),
        (AngleUnit.ARCMINUTE, 90.0, 1.5),
        (AngleUnit.ARCSECOND, 5400.0, 1.5),
        (AngleUnit.RADIAN, math.pi, 180.0),
    ],
)
def test_degree_property(unit: AngleUnit, value: float, expected_degree: float) -> None:
    assert np.allclose(make_angle([value], unit).degree, np.array([expected_degree]))


@pytest.mark.parametrize(
    ("unit", "value", "expected_radian"),
    [
        (AngleUnit.DEGREE, 180.0, math.pi),
        (AngleUnit.ARCMINUTE, 5400.0, math.pi / 2.0),
        (AngleUnit.ARCSECOND, 324000.0, math.pi / 2.0),
        (AngleUnit.RADIAN, 1.0, 1.0),
    ],
)
def test_radian_property(unit: AngleUnit, value: float, expected_radian: float) -> None:
    assert np.allclose(make_angle([value], unit).radian, np.array([expected_radian]))


def test_radian_property_returns_value_when_already_radian() -> None:
    angle: Angle = make_angle([1.0], AngleUnit.RADIAN)
    assert angle.radian is angle.value


def test_degree_property_on_integer_array() -> None:
    angle: Angle = Angle(value=np.array([90, 180]), unit=AngleUnit.DEGREE)
    assert np.allclose(angle.degree, np.array([90.0, 180.0]))
    assert np.allclose(angle.radian, np.array([math.pi / 2.0, math.pi]))


@pytest.mark.parametrize(
    ("source_unit", "target_unit"),
    list(itertools.product(ALL_ANGLE_UNITS, ALL_ANGLE_UNITS)),
)
def test_convert_unit_all_pairs(source_unit: AngleUnit, target_unit: AngleUnit) -> None:
    angle: Angle = make_angle([0.0, 1.0, 2.5], source_unit)
    expected_degree: NumericArray = angle.degree
    angle.convert_unit(target_unit)
    assert angle.unit == target_unit
    assert np.allclose(angle.degree, expected_degree)
    assert np.allclose(angle.value, expected_degree / DEGREES_PER_UNIT[target_unit])


def test_convert_unit_defaults_to_degree() -> None:
    angle: Angle = make_angle([math.pi], AngleUnit.RADIAN)
    angle.convert_unit()
    assert angle.unit == AngleUnit.DEGREE
    assert np.allclose(angle.value, np.array([180.0]))


def test_convert_unit_to_same_unit_keeps_value() -> None:
    value: NumericArray = np.array([12.0])
    angle: Angle = Angle(value=value, unit=AngleUnit.ARCMINUTE)
    angle.convert_unit(AngleUnit.ARCMINUTE)
    assert angle.value is value


def test_convert_unit_round_trip_is_stable() -> None:
    angle: Angle = make_angle([12.345, 359.999], AngleUnit.DEGREE)
    for unit in [AngleUnit.RADIAN, AngleUnit.ARCSECOND, AngleUnit.ARCMINUTE, AngleUnit.DEGREE]:
        angle.convert_unit(unit)
    assert np.allclose(angle.value, np.array([12.345, 359.999]))


def make_sexagesimal(
    degrees: list[float],
    minutes: list[float],
    seconds: list[float],
    is_negative: list[bool] | None = None,
) -> DegreesMinutesSeconds:
    return DegreesMinutesSeconds(
        degrees=np.array(degrees),
        minutes=np.array(minutes),
        seconds=np.array(seconds),
        is_negative=np.array([False] * len(degrees) if is_negative is None else is_negative, dtype=np.bool_),
    )


def test_from_degrees_minutes_seconds() -> None:
    angle: Angle = Angle.from_degrees_minutes_seconds(
        make_sexagesimal([35.0, 139.0, 0.0], [40.0, 45.0, 0.0], [30.36, 0.0, 0.0])
    )
    assert angle.unit == AngleUnit.DEGREE
    assert np.allclose(angle.value, np.array([35.6751, 139.75, 0.0]))


def test_from_degrees_minutes_seconds_accepts_integer_arrays() -> None:
    angle: Angle = Angle.from_degrees_minutes_seconds(
        DegreesMinutesSeconds(
            degrees=np.array([10]),
            minutes=np.array([30]),
            seconds=np.array([36]),
            is_negative=np.array([False]),
        )
    )
    assert np.allclose(angle.degree, np.array([10.51]))


def test_from_degrees_minutes_seconds_accepts_empty_arrays() -> None:
    assert len(Angle.from_degrees_minutes_seconds(make_sexagesimal([], [], []))) == 0


def test_negated_degrees_minutes_seconds_expresses_southern_direction() -> None:
    southern_latitude: Angle = -Angle.from_degrees_minutes_seconds(make_sexagesimal([0.0], [30.0], [0.0]))
    assert np.allclose(southern_latitude.degree, np.array([-0.5]))


def test_from_normalized_degrees_minutes_seconds_matches_total() -> None:
    angle: Angle = Angle.from_degrees_minutes_seconds(
        DegreesMinutesSeconds.normalized(
            degrees=np.array([1.5]),
            minutes=np.array([75.0]),
            seconds=np.array([90.0]),
        )
    )
    assert np.allclose(angle.degree, np.array([1.5 + 75.0 / 60.0 + 90.0 / 3600.0]))


def test_from_degrees_minutes_seconds_applies_sign() -> None:
    angle: Angle = Angle.from_degrees_minutes_seconds(
        make_sexagesimal([35.0, 0.0, 139.0], [40.0, 30.0, 45.0], [30.36, 0.0, 0.0], [True, True, False])
    )
    assert np.allclose(angle.degree, np.array([-35.6751, -0.5, 139.75]))


@pytest.mark.parametrize(
    ("degree", "expected"),
    [
        (35.6751, (35.0, 40.0, 30.36, False)),
        (-139.75, (139.0, 45.0, 0.0, True)),
        (-0.5, (0.0, 30.0, 0.0, True)),
        (0.0, (0.0, 0.0, 0.0, False)),
        (1.0 / 3600.0, (0.0, 0.0, 1.0, False)),
        (720.25, (720.0, 15.0, 0.0, False)),
    ],
)
def test_degrees_minutes_seconds_property(degree: float, expected: tuple[float, float, float, bool]) -> None:
    sexagesimal: DegreesMinutesSeconds = make_angle([degree], AngleUnit.DEGREE).degrees_minutes_seconds
    assert np.allclose(sexagesimal.degrees, np.array([expected[0]]))
    assert np.allclose(sexagesimal.minutes, np.array([expected[1]]))
    assert np.allclose(sexagesimal.seconds, np.array([expected[2]]))
    assert np.array_equal(sexagesimal.is_negative, np.array([expected[3]]))


@pytest.mark.parametrize("unit", ALL_ANGLE_UNITS)
def test_degrees_minutes_seconds_round_trip(unit: AngleUnit) -> None:
    angle: Angle = make_angle([0.0, 1.0, -2.5, 123.456789, -0.001], unit)
    restored: Angle = Angle.from_degrees_minutes_seconds(angle.degrees_minutes_seconds)
    assert restored == angle


def test_degrees_minutes_seconds_property_stays_canonical_near_boundary() -> None:
    sexagesimal: DegreesMinutesSeconds = make_angle([359.9999999, -0.99999999], AngleUnit.DEGREE).degrees_minutes_seconds
    assert np.all(sexagesimal.minutes < 60)
    assert np.all(sexagesimal.seconds < 60)
    assert np.all(sexagesimal.seconds >= 0)


def test_degrees_minutes_seconds_property_absorbs_floating_point_noise() -> None:
    sexagesimal: DegreesMinutesSeconds = make_angle([math.pi / 6], AngleUnit.RADIAN).degrees_minutes_seconds
    assert np.array_equal(sexagesimal.degrees, np.array([30.0]))
    assert np.array_equal(sexagesimal.minutes, np.array([0.0]))
    assert np.array_equal(sexagesimal.seconds, np.array([0.0]))


def test_degrees_minutes_seconds_property_on_empty_angle() -> None:
    assert len(make_angle([], AngleUnit.RADIAN).degrees_minutes_seconds) == 0


@pytest.mark.parametrize("unit", ALL_ANGLE_UNITS)
def test_negation_keeps_unit(unit: AngleUnit) -> None:
    angle: Angle = make_angle([1.0, -2.0], unit)
    negated: Angle = -angle
    assert negated.unit == unit
    assert np.allclose(negated.value, np.array([-1.0, 2.0]))
    assert np.allclose(angle.value, np.array([1.0, -2.0]))
    assert -negated == angle


@pytest.mark.parametrize(
    ("unit", "value"),
    [
        (AngleUnit.DEGREE, 30.0),
        (AngleUnit.ARCMINUTE, 1800.0),
        (AngleUnit.ARCSECOND, 108000.0),
        (AngleUnit.RADIAN, math.pi / 6.0),
    ],
)
def test_trigonometric_functions(unit: AngleUnit, value: float) -> None:
    angle: Angle = make_angle([value], unit)
    assert np.allclose(angle.sin, np.array([0.5]))
    assert np.allclose(angle.cos, np.array([math.sqrt(3.0) / 2.0]))
    assert np.allclose(angle.tan, np.array([1.0 / math.sqrt(3.0)]))


def test_trigonometric_functions_on_multiple_values() -> None:
    angle: Angle = make_angle([0.0, 90.0, 180.0, 270.0], AngleUnit.DEGREE)
    assert np.allclose(angle.sin, np.array([0.0, 1.0, 0.0, -1.0]))
    assert np.allclose(angle.cos, np.array([1.0, 0.0, -1.0, 0.0]))


def test_addition_mixes_units_and_returns_radian() -> None:
    total: Angle = make_angle([90.0], AngleUnit.DEGREE) + make_angle([5400.0], AngleUnit.ARCMINUTE)
    assert total.unit == AngleUnit.RADIAN
    assert np.allclose(total.value, np.array([math.pi]))


def test_subtraction_mixes_units_and_returns_radian() -> None:
    difference: Angle = make_angle([90.0], AngleUnit.DEGREE) - make_angle([3600.0], AngleUnit.ARCSECOND)
    assert difference.unit == AngleUnit.RADIAN
    assert np.allclose(difference.degree, np.array([89.0]))


def test_subtraction_allows_negative_result() -> None:
    difference: Angle = make_angle([10.0], AngleUnit.DEGREE) - make_angle([30.0], AngleUnit.DEGREE)
    assert np.allclose(difference.degree, np.array([-20.0]))


def test_addition_is_elementwise() -> None:
    total: Angle = make_angle([10.0, 20.0], AngleUnit.DEGREE) + make_angle([1.0, 2.0], AngleUnit.DEGREE)
    assert np.allclose(total.degree, np.array([11.0, 22.0]))


def test_equality_across_units() -> None:
    assert make_angle([180.0], AngleUnit.DEGREE) == make_angle([math.pi], AngleUnit.RADIAN)
    assert make_angle([1.0, 2.0], AngleUnit.DEGREE) == make_angle([60.0, 120.0], AngleUnit.ARCMINUTE)


def test_inequality_on_different_values() -> None:
    assert make_angle([1.0], AngleUnit.DEGREE) != make_angle([2.0], AngleUnit.DEGREE)


def test_inequality_on_different_shapes() -> None:
    assert make_angle([1.0], AngleUnit.DEGREE) != make_angle([1.0, 1.0], AngleUnit.DEGREE)


def test_inequality_with_other_types() -> None:
    angle: Angle = make_angle([1.0], AngleUnit.DEGREE)
    assert angle != 1.0
    assert angle != np.array([1.0])


def test_len() -> None:
    assert len(make_angle([1.0, 2.0, 3.0], AngleUnit.DEGREE)) == 3
