# speed

## Overview

This module provides utilities for working with speed values and units, including unit conversion. A speed may be negative, as a signed velocity along an axis or the difference of two speeds.

## Components

| Component | Description |
|-----------|-------------|
| [unit.py](./unit.py) | Enum defining speed units (m/s, km/h, mph, ft/s, kn) with conversion to meters per second. |
| [speed.py](./speed.py) | Container class for speed values with unit conversion and arithmetic. |

## Examples

```python
import numpy as np

from units import Length, LengthUnit, MetricPrefix, Time, TimeUnit

distance = Length(value=np.array([100.0]), unit=LengthUnit.M, prefix=MetricPrefix.KILO)
duration = Time(value=np.array([2.0]), unit=TimeUnit.HR)

speed = distance / duration
print(speed.kilometer_per_hour)  # [50.]
```
