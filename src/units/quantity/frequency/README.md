# frequency

## Overview

This module provides utilities for working with frequency values and units, including unit conversion and the period. A unit and a `MetricPrefix` are given separately, so a kilohertz is `HERTZ` with `KILO`. Only the hertz takes a prefix.

## Components

| Component | Description |
|-----------|-------------|
| [unit.py](./unit.py) | Enum defining frequency units without prefixes (Hz, rpm, bpm) with conversion to hertz. |
| [frequency.py](./frequency.py) | Container class for frequency values with a unit, a prefix, unit conversion and the period. |

## Examples

```python
import numpy as np

from units import Frequency, FrequencyUnit, Speed, SpeedUnit

pitch = Frequency(value=np.array([440.0]), unit=FrequencyUnit.HERTZ)
print(pitch.kilohertz)  # [0.44]

speed_of_sound = Speed(value=np.array([340.0]), unit=SpeedUnit.METER_PER_SECOND)
wavelength = speed_of_sound / pitch
print(wavelength.meter)  # [0.77272727]
```
