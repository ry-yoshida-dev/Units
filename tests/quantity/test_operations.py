from __future__ import annotations

import numpy as np
import pytest

from units import (
    Area,
    AreaUnit,
    Frequency,
    FrequencyUnit,
    Length,
    LengthUnit,
    Mass,
    MassUnit,
    MetricPrefix,
    Speed,
    SpeedUnit,
    Time,
    TimeUnit,
    Volume,
    VolumeUnit,
)


def meters(*values: float) -> Length:
    return Length(value=np.array(values), unit=LengthUnit.M)


def square_meters(*values: float) -> Area:
    return Area(value=np.array(values), unit=AreaUnit.SQUARE_METER)


def cubic_meters(*values: float) -> Volume:
    return Volume(value=np.array(values), unit=VolumeUnit.CUBIC_METER)


def seconds(*values: float) -> Time:
    return Time(value=np.array(values), unit=TimeUnit.S)


def test_length_times_length_is_area() -> None:
    kilometer = Length(
        value=np.array([1.0]), unit=LengthUnit.M, prefix=MetricPrefix.KILO
    )
    area = kilometer * meters(2.0)
    assert isinstance(area, Area)
    assert area == square_meters(2000.0)


def test_length_times_area_and_area_times_length_are_volume() -> None:
    for volume in [meters(2.0) * square_meters(3.0), square_meters(3.0) * meters(2.0)]:
        assert isinstance(volume, Volume)
        assert volume == cubic_meters(6.0)


def test_area_divided_by_length_is_length() -> None:
    length = square_meters(6.0) / meters(2.0)
    assert isinstance(length, Length)
    assert length == meters(3.0)


def test_volume_divided_by_area_is_length() -> None:
    length = cubic_meters(6.0) / square_meters(2.0)
    assert isinstance(length, Length)
    assert length == meters(3.0)


def test_volume_divided_by_length_is_area() -> None:
    area = cubic_meters(6.0) / meters(2.0)
    assert isinstance(area, Area)
    assert area == square_meters(3.0)


def test_length_divided_by_time_is_speed() -> None:
    kilometers = Length(
        value=np.array([100.0]), unit=LengthUnit.M, prefix=MetricPrefix.KILO
    )
    speed = kilometers / Time(value=np.array([2.0]), unit=TimeUnit.HR)
    assert isinstance(speed, Speed)
    assert np.allclose(speed.kilometer_per_hour, np.array([50.0]))


def test_length_divided_by_speed_is_time() -> None:
    duration = meters(100.0) / Speed(
        value=np.array([5.0]), unit=SpeedUnit.METER_PER_SECOND
    )
    assert isinstance(duration, Time)
    assert duration == seconds(20.0)


def test_speed_times_time_is_length_in_either_order() -> None:
    speed = Speed(value=np.array([36.0]), unit=SpeedUnit.KILOMETER_PER_HOUR)
    for length in [speed * seconds(10.0), seconds(10.0) * speed]:
        assert isinstance(length, Length)
        assert length == meters(100.0)


def test_negative_distance_is_rejected() -> None:
    speed = Speed(value=np.array([-1.0]), unit=SpeedUnit.METER_PER_SECOND)
    with pytest.raises(ValueError, match="must not be negative"):
        _ = speed * seconds(1.0)


def test_operations_are_elementwise() -> None:
    area = meters(1.0, 2.0) * meters(3.0, 4.0)
    assert np.allclose(area.square_meter, np.array([3.0, 8.0]))


def hertz(*values: float) -> Frequency:
    return Frequency(value=np.array(values), unit=FrequencyUnit.HERTZ)


def grams(*values: float) -> Mass:
    return Mass(value=np.array(values), unit=MassUnit.GRAM)


def speed_of_sound() -> Speed:
    return Speed(value=np.array([340.0]), unit=SpeedUnit.METER_PER_SECOND)


def test_speed_divided_by_frequency_is_the_wavelength() -> None:
    wavelength = speed_of_sound() / hertz(440.0)
    assert isinstance(wavelength, Length)
    assert wavelength == meters(340.0 / 440.0)


def test_speed_divided_by_length_is_frequency() -> None:
    frequency = speed_of_sound() / meters(2.0)
    assert isinstance(frequency, Frequency)
    assert frequency == hertz(170.0)


def test_length_times_frequency_is_speed_in_either_order() -> None:
    for speed in [meters(2.0) * hertz(170.0), hertz(170.0) * meters(2.0)]:
        assert isinstance(speed, Speed)
        assert speed == speed_of_sound()


def test_frequency_times_time_is_the_number_of_cycles_in_either_order() -> None:
    for cycles in [hertz(440.0) * seconds(2.0), seconds(2.0) * hertz(440.0)]:
        assert isinstance(cycles, np.ndarray)
        assert np.allclose(cycles, np.array([880.0]))


def test_addition_and_subtraction_of_different_quantities_are_rejected() -> None:
    with pytest.raises(TypeError):
        _ = meters(1.0) + grams(1.0)  # type: ignore[operator]  # pyright: ignore[reportOperatorIssue, reportUnknownVariableType]
    with pytest.raises(TypeError):
        _ = meters(1.0) - grams(1.0)  # type: ignore[operator]  # pyright: ignore[reportOperatorIssue, reportUnknownVariableType]


def test_multiplication_without_a_defined_result_is_rejected() -> None:
    with pytest.raises(TypeError):
        _ = meters(1.0) * grams(1.0)  # type: ignore[operator]  # pyright: ignore[reportOperatorIssue, reportUnknownVariableType]
    with pytest.raises(TypeError):
        _ = grams(1.0) * grams(1.0)  # type: ignore[operator]  # pyright: ignore[reportOperatorIssue, reportUnknownVariableType]


def test_division_without_a_defined_result_is_rejected() -> None:
    with pytest.raises(TypeError):
        _ = meters(1.0) / grams(1.0)  # type: ignore[operator]  # pyright: ignore[reportOperatorIssue, reportUnknownVariableType]


def test_different_quantities_with_equal_base_values_are_not_equal() -> None:
    assert meters(1.0) != grams(1.0)


def test_negative_speed_has_no_wavelength_or_frequency() -> None:
    speed = Speed(value=np.array([-1.0]), unit=SpeedUnit.METER_PER_SECOND)
    with pytest.raises(ValueError, match="must not be negative"):
        _ = speed / Frequency(value=np.array([1.0]), unit=FrequencyUnit.HERTZ)
    with pytest.raises(ValueError, match="must not be negative"):
        _ = speed / Length(value=np.array([1.0]), unit=LengthUnit.M)
