# units

## Overview

This package provides utilities for working with physical quantities and units.

SI prefixes, such as kilo and hecto, are kept apart from the units they scale. A prefix applies to the length of a unit before the unit is raised to its power, so kilo makes a square meter 10^6 times larger and an are only 10^3 times. `MetricPrefix.NONE` stands for the unit itself.

## Components

| Component | Description |
|-----------|-------------|
| [types.py](./types.py) | Shared NumPy array type aliases for numeric physical quantity values. |
| [prefix.py](./prefix.py) | Enum defining the SI prefixes from peta to femto, plus `NONE` for no prefix, and their factors. |
| [quantity](./quantity/) | Physical quantities, each with a container class and a unit enum. |

## Usage

```python
import numpy as np

from units import Angle, AngleUnit, Length, LengthUnit, MetricPrefix, Time, TimeUnit

distance = Length(value=np.array([1.2]), unit=LengthUnit.M, prefix=MetricPrefix.KILO)
heading = Angle(value=np.array([90.0]), unit=AngleUnit.DEGREE)
duration = Time(value=np.array([2.0]), unit=TimeUnit.HR)

print(distance.meter)   # [1200.]
print(heading.radian)   # [1.57079633]
print(duration.second)  # [7200.]

speed = distance / duration
print(speed.kilometer_per_hour)  # [0.6]

print(MetricPrefix.KILO.factor)  # 1000.0
print(MetricPrefix.HECTO.value)  # h
```
