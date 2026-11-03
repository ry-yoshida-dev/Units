from __future__ import annotations

import numpy as np
import pytest

from units import MetricPrefix, Volume, VolumeUnit

ALL_UNITS: list[tuple[VolumeUnit, MetricPrefix]] = [
    (VolumeUnit.CUBIC_METER, MetricPrefix.NONE),
    (VolumeUnit.CUBIC_METER, MetricPrefix.CENTI),
    (VolumeUnit.LITER, MetricPrefix.NONE),
    (VolumeUnit.LITER, MetricPrefix.MILLI),
    (VolumeUnit.CUBIC_FOOT, MetricPrefix.NONE),
    (VolumeUnit.US_GALLON, MetricPrefix.NONE),
    (VolumeUnit.IMPERIAL_GALLON, MetricPrefix.NONE),
    (VolumeUnit.GO, MetricPrefix.NONE),
    (VolumeUnit.SHO, MetricPrefix.NONE),
]


def make_volume(values: list[float], unit: VolumeUnit, prefix: MetricPrefix = MetricPrefix.NONE) -> Volume:
    return Volume(value=np.array(values), unit=unit, prefix=prefix)


@pytest.mark.parametrize(
    ("unit", "prefix", "cubic_meters", "symbol"),
    [
        (VolumeUnit.CUBIC_METER, MetricPrefix.NONE, 1.0, "m3"),
        (VolumeUnit.CUBIC_METER, MetricPrefix.CENTI, 1e-6, "cm3"),
        (VolumeUnit.CUBIC_METER, MetricPrefix.KILO, 1e9, "km3"),
        (VolumeUnit.LITER, MetricPrefix.NONE, 1e-3, "L"),
        (VolumeUnit.LITER, MetricPrefix.MILLI, 1e-6, "mL"),
        (VolumeUnit.CUBIC_FOOT, MetricPrefix.NONE, 0.3048**3, "ft3"),
        (VolumeUnit.US_GALLON, MetricPrefix.NONE, 231 * 0.0254**3, "gal"),
        (VolumeUnit.IMPERIAL_GALLON, MetricPrefix.NONE, 4.54609e-3, "imp gal"),
        (VolumeUnit.GO, MetricPrefix.NONE, 2401 / 1331 / 10 * 1e-3, "go"),
        (VolumeUnit.SHO, MetricPrefix.NONE, 2401 / 1331 * 1e-3, "sho"),
    ],
)
def test_prefix_is_raised_to_the_power_of_the_unit(
    unit: VolumeUnit, prefix: MetricPrefix, cubic_meters: float, symbol: str
) -> None:
    assert unit.prefixed_factor(prefix) == pytest.approx(cubic_meters)
    assert unit.symbol(prefix) == symbol


@pytest.mark.parametrize(
    "unit",
    [VolumeUnit.CUBIC_FOOT, VolumeUnit.US_GALLON, VolumeUnit.IMPERIAL_GALLON, VolumeUnit.GO, VolumeUnit.SHO],
)
def test_units_outside_the_metric_system_take_no_prefix(unit: VolumeUnit) -> None:
    with pytest.raises(ValueError, match="no prefix"):
        _ = make_volume([1.0], unit, MetricPrefix.MILLI)


@pytest.mark.parametrize("values", [[-1.0], [1.0, -0.001]])
def test_volume_rejects_negative_values(values: list[float]) -> None:
    with pytest.raises(ValueError, match="must not be negative"):
        _ = make_volume(values, VolumeUnit.LITER)


def test_named_unit_properties() -> None:
    volume: Volume = make_volume([2.0], VolumeUnit.CUBIC_METER)
    assert np.allclose(volume.cubic_meter, np.array([2.0]))
    assert np.allclose(volume.cubic_centimeter, np.array([2e6]))
    assert np.allclose(volume.liter, np.array([2000.0]))
    assert np.allclose(volume.milliliter, np.array([2e6]))
    assert np.allclose(volume.cubic_foot, np.array([2.0 / 0.3048**3]))
    assert np.allclose(volume.us_gallon, np.array([2000.0 / 3.785411784]))
    assert np.allclose(volume.imperial_gallon, np.array([2000.0 / 4.54609]))
    assert np.allclose(volume.sho, np.array([2000.0 * 1331 / 2401]))
    assert np.allclose(volume.go, np.array([20000.0 * 1331 / 2401]))


@pytest.mark.parametrize("source", ALL_UNITS)
@pytest.mark.parametrize("target", ALL_UNITS)
def test_convert_unit_all_pairs(
    source: tuple[VolumeUnit, MetricPrefix], target: tuple[VolumeUnit, MetricPrefix]
) -> None:
    volume: Volume = make_volume([0.0, 1.0, 2.5], *source)
    expected_cubic_meter = volume.cubic_meter
    volume.convert_unit(*target)
    assert (volume.unit, volume.prefix) == target
    assert np.allclose(volume.cubic_meter, expected_cubic_meter)


def test_arithmetic() -> None:
    liter: Volume = make_volume([1.0], VolumeUnit.LITER)
    half: Volume = make_volume([500.0], VolumeUnit.LITER, MetricPrefix.MILLI)
    assert (liter + half) == make_volume([1.5], VolumeUnit.LITER)
    assert (liter - half) == half
    assert (2 * half) == liter
    assert (half * 2) == liter
    assert np.allclose(np.asarray(liter / half), np.array([2.0]))
    halved = liter / 2
    assert isinstance(halved, Volume)
    assert halved == half


def test_string_representations() -> None:
    volume: Volume = make_volume([1.5], VolumeUnit.LITER, MetricPrefix.MILLI)
    assert str(volume) == "[1.5] mL"
    assert repr(volume) == "Volume(value=[1.5], unit=VolumeUnit.LITER, prefix=MetricPrefix.MILLI)"


def test_equality_requires_a_volume_of_the_same_shape() -> None:
    assert make_volume([1.0], VolumeUnit.LITER) != make_volume([1.0, 1.0], VolumeUnit.LITER)
    assert make_volume([1.0], VolumeUnit.LITER) != "1 L"
