from __future__ import annotations

import itertools

import numpy as np
import pytest

from units import Speed, SpeedUnit

METERS_PER_SECOND_PER_UNIT: dict[SpeedUnit, float] = {
    SpeedUnit.METER_PER_SECOND: 1.0,
    SpeedUnit.KILOMETER_PER_HOUR: 1 / 3.6,
    SpeedUnit.MILE_PER_HOUR: 1609.344 / 3600,
    SpeedUnit.FOOT_PER_SECOND: 0.3048,
    SpeedUnit.KNOT: 1852 / 3600,
}


def make_speed(values: list[float], unit: SpeedUnit) -> Speed:
    return Speed(value=np.array(values), unit=unit)


@pytest.mark.parametrize("unit", list(SpeedUnit))
def test_unit_to_meter_per_second(unit: SpeedUnit) -> None:
    assert unit.factor == pytest.approx(METERS_PER_SECOND_PER_UNIT[unit])


def test_named_unit_properties() -> None:
    speed: Speed = make_speed([36.0], SpeedUnit.KILOMETER_PER_HOUR)
    assert np.allclose(speed.meter_per_second, np.array([10.0]))
    assert np.allclose(speed.kilometer_per_hour, np.array([36.0]))
    assert np.allclose(speed.mile_per_hour, np.array([36000.0 / 1609.344]))
    assert np.allclose(speed.foot_per_second, np.array([10.0 / 0.3048]))
    assert np.allclose(speed.knot, np.array([36000.0 / 1852.0]))


def test_negative_speed_is_allowed() -> None:
    assert np.allclose(
        make_speed([-3.6], SpeedUnit.KILOMETER_PER_HOUR).meter_per_second,
        np.array([-1.0]),
    )


@pytest.mark.parametrize(
    ("source", "target"), list(itertools.product(SpeedUnit, SpeedUnit))
)
def test_convert_unit_all_pairs(source: SpeedUnit, target: SpeedUnit) -> None:
    speed: Speed = make_speed([0.0, 1.0, 2.5], source)
    expected = speed.meter_per_second
    speed.convert_unit(target)
    assert speed.unit == target
    assert np.allclose(speed.meter_per_second, expected)


def test_arithmetic() -> None:
    fast: Speed = make_speed([36.0], SpeedUnit.KILOMETER_PER_HOUR)
    slow: Speed = make_speed([5.0], SpeedUnit.METER_PER_SECOND)
    assert (fast + slow) == make_speed([15.0], SpeedUnit.METER_PER_SECOND)
    assert (fast - slow) == slow
    assert (slow - fast) == make_speed([-5.0], SpeedUnit.METER_PER_SECOND)
    assert (2 * slow) == fast
    assert (slow * 2) == fast
    assert np.allclose(np.asarray(fast / slow), np.array([2.0]))
    halved = fast / 2
    assert isinstance(halved, Speed)
    assert halved.unit == SpeedUnit.KILOMETER_PER_HOUR
    assert halved == slow


def test_string_representations() -> None:
    speed: Speed = make_speed([1.5], SpeedUnit.KNOT)
    assert str(speed) == "[1.5] kn"
    assert (
        repr(speed)
        == "Speed(value=[1.5], unit=SpeedUnit.KNOT, prefix=MetricPrefix.NONE)"
    )


def test_equality_requires_a_speed_of_the_same_shape() -> None:
    assert make_speed([1.0], SpeedUnit.KNOT) != make_speed([1.0, 1.0], SpeedUnit.KNOT)
    assert make_speed([1.0], SpeedUnit.KNOT) != "1 kn"
