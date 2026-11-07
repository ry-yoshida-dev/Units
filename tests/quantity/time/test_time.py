from __future__ import annotations

import itertools

import numpy as np
import pytest

from units import MetricPrefix, NumericArray, Time, TimeUnit

ALL_TIME_UNITS: list[TimeUnit] = list(TimeUnit)

SECONDS_PER_UNIT: dict[TimeUnit, float] = {
    TimeUnit.S: 1.0,
    TimeUnit.MIN: 60.0,
    TimeUnit.HR: 3600.0,
    TimeUnit.DAY: 86400.0,
    TimeUnit.WEEK: 604800.0,
}


def make_time(
    values: list[float], unit: TimeUnit, prefix: MetricPrefix = MetricPrefix.NONE
) -> Time:
    return Time(value=np.array(values), unit=unit, prefix=prefix)


@pytest.mark.parametrize(
    ("prefix", "seconds", "symbol"),
    [
        (MetricPrefix.NONE, 1.0, "s"),
        (MetricPrefix.MILLI, 1e-3, "ms"),
        (MetricPrefix.MICRO, 1e-6, "µs"),
        (MetricPrefix.NANO, 1e-9, "ns"),
    ],
)
def test_prefix_scales_the_second(
    prefix: MetricPrefix, seconds: float, symbol: str
) -> None:
    assert TimeUnit.S.prefixed_factor(prefix) == pytest.approx(seconds)
    assert TimeUnit.S.symbol(prefix) == symbol


@pytest.mark.parametrize("unit", [unit for unit in TimeUnit if unit is not TimeUnit.S])
def test_only_the_second_takes_a_prefix(unit: TimeUnit) -> None:
    with pytest.raises(ValueError, match="no prefix"):
        _ = make_time([1.0], unit, MetricPrefix.MILLI)


@pytest.mark.parametrize("unit", ALL_TIME_UNITS)
def test_unit_to_second(unit: TimeUnit) -> None:
    assert unit.factor == pytest.approx(SECONDS_PER_UNIT[unit])


@pytest.mark.parametrize("unit", ALL_TIME_UNITS)
def test_second_property(unit: TimeUnit) -> None:
    duration: Time = make_time([2.0, 3.0], unit)
    assert np.allclose(duration.second, np.array([2.0, 3.0]) * SECONDS_PER_UNIT[unit])


def test_named_unit_properties() -> None:
    duration: Time = make_time([1.0], TimeUnit.DAY)
    assert np.allclose(duration.ms, np.array([86400000.0]))
    assert np.allclose(duration.minute, np.array([1440.0]))
    assert np.allclose(duration.hour, np.array([24.0]))
    assert np.allclose(duration.day, np.array([1.0]))
    assert np.allclose(duration.week, np.array([1.0 / 7.0]))
    assert np.allclose(duration.microsecond, np.array([86400e6]))
    assert np.allclose(duration.nanosecond, np.array([86400e9]))


def test_negative_duration_is_allowed() -> None:
    assert np.allclose(make_time([-1.0], TimeUnit.MIN).second, np.array([-60.0]))


@pytest.mark.parametrize(
    ("source_unit", "target_unit"),
    list(itertools.product(ALL_TIME_UNITS, ALL_TIME_UNITS)),
)
def test_convert_unit_all_pairs(source_unit: TimeUnit, target_unit: TimeUnit) -> None:
    duration: Time = make_time([0.0, 1.0, 2.5], source_unit)
    expected_second: NumericArray = duration.second
    duration.convert_unit(target_unit)
    assert duration.unit == target_unit
    assert np.allclose(duration.second, expected_second)
    assert np.allclose(duration.value, expected_second / SECONDS_PER_UNIT[target_unit])


def test_convert_unit_changes_the_prefix() -> None:
    duration: Time = make_time([2.0], TimeUnit.S)
    duration.convert_unit(TimeUnit.S, MetricPrefix.MILLI)
    assert duration.prefix is MetricPrefix.MILLI
    assert np.allclose(duration.value, np.array([2000.0]))


def test_scalar_operations_keep_the_prefix() -> None:
    duration: Time = make_time([4.0], TimeUnit.S, MetricPrefix.MILLI)
    for result in [duration * 2.0, 2.0 * duration, duration / 2.0]:
        assert isinstance(result, Time)
        assert result.prefix is MetricPrefix.MILLI


def test_convert_unit_defaults_to_second() -> None:
    duration: Time = make_time([2.0], TimeUnit.MIN)
    duration.convert_unit()
    assert duration.unit == TimeUnit.S
    assert np.allclose(duration.value, np.array([120.0]))


def test_convert_unit_to_same_unit_keeps_value() -> None:
    value: NumericArray = np.array([3.0])
    duration: Time = Time(value=value, unit=TimeUnit.HR)
    duration.convert_unit(TimeUnit.HR)
    assert duration.value is value


def test_addition_mixes_units_and_returns_second() -> None:
    total: Time = make_time([1.0], TimeUnit.HR) + make_time([1800.0], TimeUnit.S)
    assert total.unit == TimeUnit.S
    assert np.allclose(total.value, np.array([5400.0]))


def test_subtraction_mixes_units_and_returns_second() -> None:
    difference: Time = make_time([1.0], TimeUnit.HR) - make_time([30.0], TimeUnit.MIN)
    assert difference.unit == TimeUnit.S
    assert np.allclose(difference.value, np.array([1800.0]))


def test_subtraction_allows_negative_result() -> None:
    difference: Time = make_time([1.0], TimeUnit.S) - make_time([2.0], TimeUnit.S)
    assert np.allclose(difference.value, np.array([-1.0]))


def test_multiplication_by_scalar_keeps_unit() -> None:
    duration: Time = make_time([1.0], TimeUnit.HR)
    for product in [duration * 2.0, 2.0 * duration]:
        assert product.unit == TimeUnit.HR
        assert np.allclose(product.second, np.array([7200.0]))


def test_multiplication_by_array_is_elementwise() -> None:
    product: Time = make_time([1.0, 2.0], TimeUnit.S) * np.array([3.0, 4.0])
    assert np.allclose(product.value, np.array([3.0, 8.0]))


def test_division_by_time_returns_ratio() -> None:
    ratio: Time | NumericArray = make_time([1.0], TimeUnit.HR) / make_time(
        [1800.0], TimeUnit.S
    )
    assert isinstance(ratio, np.ndarray)
    assert np.allclose(ratio, np.array([2.0]))


def test_division_by_scalar_keeps_unit() -> None:
    quotient: Time | NumericArray = make_time([1.0], TimeUnit.HR) / 2.0
    assert isinstance(quotient, Time)
    assert quotient.unit == TimeUnit.HR
    assert np.allclose(quotient.value, np.array([0.5]))


def test_division_by_array_is_elementwise() -> None:
    quotient: Time | NumericArray = make_time([4.0, 9.0], TimeUnit.S) / np.array(
        [2.0, 3.0]
    )
    assert isinstance(quotient, Time)
    assert np.allclose(quotient.value, np.array([2.0, 3.0]))


def test_equality_across_units() -> None:
    assert make_time([1000.0], TimeUnit.S, MetricPrefix.MILLI) == make_time(
        [1.0], TimeUnit.S
    )
    assert make_time([1.0], TimeUnit.DAY) == make_time([24.0], TimeUnit.HR)


def test_inequality_on_different_values() -> None:
    assert make_time([1.0], TimeUnit.S) != make_time([1.1], TimeUnit.S)


def test_inequality_on_different_shapes() -> None:
    assert make_time([1.0], TimeUnit.S) != make_time([1.0, 1.0], TimeUnit.S)


def test_inequality_with_other_types() -> None:
    assert make_time([1.0], TimeUnit.S) != 1.0


def test_string_representations() -> None:
    duration: Time = make_time([2.0], TimeUnit.HR)
    assert str(duration) == "[2.] h"
    assert (
        repr(duration) == "Time(value=[2.], unit=TimeUnit.HR, prefix=MetricPrefix.NONE)"
    )
