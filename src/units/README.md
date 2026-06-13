# units

## Overview

This package provides utilities for working with physical quantities and units.

## Components

| Component | Description |
|-----------|-------------|
| [types.py](./types.py) | Shared NumPy array type aliases for numeric physical quantity values. |
| [length](./length/) | Utilities for working with length values and length unit conversion. |
| [angle](./angle/) | Utilities for working with angle values, angle unit conversion, and trigonometric operations. |
| [time](./time/) | Utilities for working with time durations and time unit conversion. |

## Usage

```python
import numpy as np

from units import Angle, AngleUnit, Length, LengthUnit, Time, TimeUnit

distance = Length(value=np.array([1.2]), unit=LengthUnit.KM)
heading = Angle(value=np.array([90.0]), unit=AngleUnit.DEGREE)
duration = Time(value=np.array([2.0]), unit=TimeUnit.HR)

print(distance.meter)   # [1200.]
print(heading.radian)   # [1.57079633]
print(duration.second)  # [7200.]
```
