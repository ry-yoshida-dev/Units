from __future__ import annotations

import numpy as np
import pytest

from units import Frequency, FrequencyUnit, MetricPrefix, Time


def make_frequency(values: list[float], unit: FrequencyUnit, prefix: MetricPrefix = MetricPrefix.NONE) -> Frequency:
    return Frequency(value=np.array(values), unit=unit, prefix=prefix)


@pytest.mark.parametrize(
    ("unit", "prefix", "hertz", "symbol"),
    [
        (FrequencyUnit.HERTZ, MetricPrefix.NONE, 1.0, "Hz"),
        (FrequencyUnit.HERTZ, MetricPrefix.KILO, 1e3, "kHz"),
        (FrequencyUnit.RPM, MetricPrefix.NONE, 1 / 60, "rpm"),
        (FrequencyUnit.BPM, MetricPrefix.NONE, 1 / 60, "bpm"),
    ],
)
def test_conversion_factors_and_symbols(unit: FrequencyUnit, prefix: MetricPrefix, hertz: float, symbol: str) -> None:
    assert unit.prefixed_factor(prefix) == pytest.approx(hertz)
    assert unit.symbol(prefix) == symbol


@pytest.mark.parametrize("unit", [FrequencyUnit.RPM, FrequencyUnit.BPM])
def test_only_the_hertz_takes_a_prefix(unit: FrequencyUnit) -> None:
    with pytest.raises(ValueError, match="no prefix"):
        _ = make_frequency([1.0], unit, MetricPrefix.KILO)


def test_frequency_rejects_negative_values() -> None:
    with pytest.raises(ValueError, match="positive"):
        _ = make_frequency([-1.0], FrequencyUnit.HERTZ)


def test_named_unit_properties() -> None:
    frequency: Frequency = make_frequency([2000.0], FrequencyUnit.HERTZ)
    assert np.allclose(frequency.hertz, np.array([2000.0]))
    assert np.allclose(frequency.kilohertz, np.array([2.0]))
    assert np.allclose(frequency.megahertz, np.array([2e-3]))
    assert np.allclose(frequency.gigahertz, np.array([2e-6]))
    assert np.allclose(frequency.rpm, np.array([120000.0]))
    assert np.allclose(frequency.bpm, np.array([120000.0]))


def test_period_is_the_inverse_of_the_frequency() -> None:
    period: Time = make_frequency([4.0], FrequencyUnit.HERTZ).period
    assert np.allclose(period.second, np.array([0.25]))
    assert np.allclose(make_frequency([120.0], FrequencyUnit.BPM).period.second, np.array([0.5]))
