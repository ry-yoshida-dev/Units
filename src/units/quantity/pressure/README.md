# pressure

## Overview

This module provides utilities for working with pressure values and units, including unit conversion and the sound pressure level of an effective sound pressure. A unit and a `MetricPrefix` are given separately, so a hectopascal is `PASCAL` with `HECTO`. Only the pascal and the bar take a prefix. A pressure may be negative, as a gauge pressure.

## Components

| Component | Description |
|-----------|-------------|
| [unit.py](./unit.py) | Enum defining pressure units without prefixes (Pa, bar, atm, Torr, mmHg, kgf/cm², psi) with conversion to pascals. |
| [pressure.py](./pressure.py) | Container class for pressure values with a unit, a prefix and unit conversion. |

## Usage

```python
import numpy as np

from units import Pressure, PressureUnit

air = Pressure(value=np.array([1.0]), unit=PressureUnit.ATMOSPHERE)
print(air.hectopascal)  # [1013.25]

sound = Pressure(value=np.array([1.0]), unit=PressureUnit.PASCAL)
print(sound.sound_pressure_level.decibel)  # [93.97940009]
```
