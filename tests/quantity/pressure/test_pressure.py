from __future__ import annotations

import numpy as np
import pytest

from units import MetricPrefix, Pressure, PressureUnit


def make_pressure(values: list[float], unit: PressureUnit, prefix: MetricPrefix = MetricPrefix.NONE) -> Pressure:
    return Pressure(value=np.array(values), unit=unit, prefix=prefix)


@pytest.mark.parametrize(
    ("unit", "prefix", "pascals", "symbol"),
    [
        (PressureUnit.PASCAL, MetricPrefix.NONE, 1.0, "Pa"),
        (PressureUnit.PASCAL, MetricPrefix.HECTO, 100.0, "hPa"),
        (PressureUnit.BAR, MetricPrefix.NONE, 1e5, "bar"),
        (PressureUnit.BAR, MetricPrefix.MILLI, 100.0, "mbar"),
        (PressureUnit.ATMOSPHERE, MetricPrefix.NONE, 101325.0, "atm"),
        (PressureUnit.TORR, MetricPrefix.NONE, 133.32236842, "Torr"),
        (PressureUnit.MILLIMETER_OF_MERCURY, MetricPrefix.NONE, 133.322387415, "mmHg"),
        (PressureUnit.KILOGRAM_FORCE_PER_SQUARE_CENTIMETER, MetricPrefix.NONE, 98066.5, "kgf/cm2"),
        (PressureUnit.POUND_PER_SQUARE_INCH, MetricPrefix.NONE, 6894.757293, "psi"),
    ],
)
def test_conversion_factors_and_symbols(unit: PressureUnit, prefix: MetricPrefix, pascals: float, symbol: str) -> None:
    assert unit.prefixed_factor(prefix) == pytest.approx(pascals)
    assert unit.symbol(prefix) == symbol


@pytest.mark.parametrize(
    "unit",
    [unit for unit in PressureUnit if unit not in (PressureUnit.PASCAL, PressureUnit.BAR)],
)
def test_units_outside_the_metric_system_take_no_prefix(unit: PressureUnit) -> None:
    with pytest.raises(ValueError, match="no prefix"):
        _ = make_pressure([1.0], unit, MetricPrefix.KILO)


def test_gauge_pressure_may_be_negative() -> None:
    assert np.allclose(make_pressure([-1.0], PressureUnit.PASCAL, MetricPrefix.KILO).pascal, np.array([-1000.0]))


def test_named_unit_properties() -> None:
    pressure: Pressure = make_pressure([1.0], PressureUnit.ATMOSPHERE)
    assert np.allclose(pressure.pascal, np.array([101325.0]))
    assert np.allclose(pressure.hectopascal, np.array([1013.25]))
    assert np.allclose(pressure.kilopascal, np.array([101.325]))
    assert np.allclose(pressure.megapascal, np.array([0.101325]))
    assert np.allclose(pressure.bar, np.array([1.01325]))
    assert np.allclose(pressure.millibar, np.array([1013.25]))
    assert np.allclose(pressure.atmosphere, np.array([1.0]))
    assert np.allclose(pressure.torr, np.array([760.0]))
    assert np.allclose(pressure.millimeter_of_mercury, np.array([760.0]))
    assert np.allclose(pressure.kilogram_force_per_square_centimeter, np.array([1.0332274528]))
    assert np.allclose(pressure.pound_per_square_inch, np.array([14.6959488]))
