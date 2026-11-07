# sound_pressure_level

## Overview

This module provides utilities for working with sound pressure levels in air, relative to 20 micropascals, and their conversion to and from effective sound pressure. A level is logarithmic, so adding levels combines uncorrelated sources by their energy, and a level has no scalar product. Weighted levels such as dB(A) depend on the spectrum and cannot be converted from this value.

## Components

| Component | Description |
|-----------|-------------|
| [unit.py](./unit.py) | Enum defining level units (dB, B) with conversion to decibels. |
| [sound_pressure_level.py](./sound_pressure_level.py) | Container class for levels with unit conversion, conversion to `Pressure`, energy addition and subtraction. |

## Examples

```python
import numpy as np

from units import SoundPressureLevel, SoundPressureLevelUnit

source = SoundPressureLevel(value=np.array([60.0]), unit=SoundPressureLevelUnit.DECIBEL)

print((source + source).decibel)  # [63.01029996]
print(source.pressure.pascal)  # [0.02]
```
