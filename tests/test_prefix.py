from __future__ import annotations

import pytest

from units import MetricPrefix


@pytest.mark.parametrize(
    ("prefix", "factor"),
    [
        (MetricPrefix.PETA, 1e15),
        (MetricPrefix.TERA, 1e12),
        (MetricPrefix.GIGA, 1e9),
        (MetricPrefix.MEGA, 1e6),
        (MetricPrefix.KILO, 1e3),
        (MetricPrefix.HECTO, 1e2),
        (MetricPrefix.DECA, 1e1),
        (MetricPrefix.NONE, 1.0),
        (MetricPrefix.DECI, 1e-1),
        (MetricPrefix.CENTI, 1e-2),
        (MetricPrefix.MILLI, 1e-3),
        (MetricPrefix.MICRO, 1e-6),
        (MetricPrefix.NANO, 1e-9),
        (MetricPrefix.PICO, 1e-12),
        (MetricPrefix.FEMTO, 1e-15),
    ],
)
def test_factor_is_the_power_of_ten(prefix: MetricPrefix, factor: float) -> None:
    assert prefix.factor == pytest.approx(factor)
