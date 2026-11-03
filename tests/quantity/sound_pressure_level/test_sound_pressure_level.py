from __future__ import annotations

import numpy as np
import pytest

from units import (
    MetricPrefix,
    Pressure,
    PressureUnit,
    SoundPressureLevel,
    SoundPressureLevelUnit,
)


def decibels(*values: float) -> SoundPressureLevel:
    return SoundPressureLevel(value=np.array(values), unit=SoundPressureLevelUnit.DECIBEL)


def pascals(*values: float) -> Pressure:
    return Pressure(value=np.array(values), unit=PressureUnit.PASCAL)


def test_bel_is_ten_decibels() -> None:
    level = SoundPressureLevel(value=np.array([6.0]), unit=SoundPressureLevelUnit.BEL)
    assert np.allclose(level.decibel, np.array([60.0]))
    assert np.allclose(decibels(60.0).bel, np.array([6.0]))


def test_level_takes_no_prefix() -> None:
    with pytest.raises(ValueError, match="no prefix"):
        _ = SoundPressureLevel(value=np.array([1.0]), unit=SoundPressureLevelUnit.DECIBEL, prefix=MetricPrefix.KILO)


@pytest.mark.parametrize(
    ("pressure", "level"),
    [(20e-6, 0.0), (2e-4, 20.0), (1.0, 93.97940009), (2e-6, -20.0)],
)
def test_pressure_and_level_convert_both_ways(pressure: float, level: float) -> None:
    assert np.allclose(pascals(pressure).sound_pressure_level.decibel, np.array([level]))
    assert np.allclose(decibels(level).pressure.pascal, np.array([pressure]))


def test_zero_pressure_is_negative_infinity_without_a_warning() -> None:
    assert np.isneginf(pascals(0.0).sound_pressure_level.decibel).all()


def test_negative_sound_pressure_is_rejected() -> None:
    with pytest.raises(ValueError, match="must not be negative"):
        _ = pascals(-1.0).sound_pressure_level


def test_adding_equal_sources_raises_the_level_by_about_three_decibels() -> None:
    combined: SoundPressureLevel = decibels(60.0) + decibels(60.0)
    assert np.allclose(combined.decibel, np.array([60.0 + 10.0 * np.log10(2.0)]))


def test_subtraction_returns_the_difference_in_decibels() -> None:
    assert np.allclose(decibels(70.0) - decibels(60.0), np.array([10.0]))


def test_level_has_no_scalar_product() -> None:
    with pytest.raises(TypeError):
        _ = decibels(60.0) * 2.0  # type: ignore[operator]


def test_string_shows_the_symbol() -> None:
    assert str(decibels(60.0)) == "[60.] dB"
