from __future__ import annotations

import itertools

import numpy as np
import pytest

from units import NumericArray, Temperature, TemperatureUnit


def make_temperature(values: list[float], unit: TemperatureUnit) -> Temperature:
    return Temperature(value=np.array(values), unit=unit)


@pytest.mark.parametrize(
    ("unit", "value", "kelvin"),
    [
        (TemperatureUnit.KELVIN, 273.15, 273.15),
        (TemperatureUnit.CELSIUS, 0.0, 273.15),
        (TemperatureUnit.CELSIUS, 100.0, 373.15),
        (TemperatureUnit.FAHRENHEIT, 32.0, 273.15),
        (TemperatureUnit.FAHRENHEIT, 212.0, 373.15),
        (TemperatureUnit.RANKINE, 491.67, 273.15),
    ],
)
def test_conversion_to_kelvin(
    unit: TemperatureUnit, value: float, kelvin: float
) -> None:
    assert np.allclose(make_temperature([value], unit).kelvin, np.array([kelvin]))


def test_named_unit_properties() -> None:
    boiling: Temperature = make_temperature([100.0], TemperatureUnit.CELSIUS)
    assert np.allclose(boiling.celsius, np.array([100.0]))
    assert np.allclose(boiling.fahrenheit, np.array([212.0]))
    assert np.allclose(boiling.rankine, np.array([671.67]))


def test_scales_cross_at_minus_forty() -> None:
    assert make_temperature([-40.0], TemperatureUnit.CELSIUS) == make_temperature(
        [-40.0], TemperatureUnit.FAHRENHEIT
    )


@pytest.mark.parametrize(
    ("unit", "absolute_zero"),
    [
        (TemperatureUnit.KELVIN, 0.0),
        (TemperatureUnit.CELSIUS, -273.15),
        (TemperatureUnit.FAHRENHEIT, -459.67),
        (TemperatureUnit.RANKINE, 0.0),
    ],
)
def test_absolute_zero_is_the_lower_bound(
    unit: TemperatureUnit, absolute_zero: float
) -> None:
    assert np.allclose(make_temperature([absolute_zero], unit).kelvin, np.array([0.0]))
    with pytest.raises(ValueError, match="absolute zero"):
        _ = make_temperature([absolute_zero - 0.01], unit)


@pytest.mark.parametrize(
    ("source", "target"), list(itertools.product(TemperatureUnit, TemperatureUnit))
)
def test_convert_unit_all_pairs(
    source: TemperatureUnit, target: TemperatureUnit
) -> None:
    temperature: Temperature = make_temperature([300.0, 500.0], source)
    expected = temperature.kelvin
    temperature.convert_unit(target)
    assert temperature.unit == target
    assert np.allclose(temperature.kelvin, expected)


def test_convert_unit_defaults_to_kelvin() -> None:
    temperature: Temperature = make_temperature([0.0], TemperatureUnit.CELSIUS)
    temperature.convert_unit()
    assert temperature.unit == TemperatureUnit.KELVIN
    assert np.allclose(temperature.value, np.array([273.15]))


def test_convert_unit_to_same_unit_keeps_value() -> None:
    value: NumericArray = np.array([3.0])
    temperature: Temperature = Temperature(value=value, unit=TemperatureUnit.CELSIUS)
    temperature.convert_unit(TemperatureUnit.CELSIUS)
    assert temperature.value is value


def test_subtraction_returns_the_difference_in_kelvin() -> None:
    difference: NumericArray = make_temperature(
        [212.0], TemperatureUnit.FAHRENHEIT
    ) - make_temperature([0.0], TemperatureUnit.CELSIUS)
    assert np.allclose(difference, np.array([100.0]))


def test_string_representations() -> None:
    temperature: Temperature = make_temperature([1.5], TemperatureUnit.CELSIUS)
    assert str(temperature) == "[1.5] °C"
    assert (
        repr(temperature)
        == "Temperature(value=[1.5], unit=TemperatureUnit.CELSIUS, prefix=MetricPrefix.NONE)"
    )


def test_equality_requires_a_temperature_of_the_same_shape() -> None:
    assert make_temperature([1.0], TemperatureUnit.KELVIN) != make_temperature(
        [1.0, 1.0], TemperatureUnit.KELVIN
    )
    assert make_temperature([1.0], TemperatureUnit.KELVIN) != "1 K"
