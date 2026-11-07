# time

## Overview

This module provides utilities for working with time durations and units, including conversion between seconds, minutes, hours, days, and weeks, and arithmetic on `Time` values backed by NumPy arrays. A unit and a `MetricPrefix` are given separately, so a millisecond is `S` with `MILLI`. Only the second takes a prefix.

## Components

| Component | Description |
|-----------|-------------|
| [unit.py](./unit.py) | Enum defining time units without prefixes (`s`, `min`, `h`, `day`, `week`) with conversion factors to seconds. |
| [time.py](./time.py) | Container class for durations with a unit, a prefix, unit conversion, accessors in each supported unit, and basic arithmetic. |

## Examples

```python
import numpy as np

from units import Time, TimeUnit

warmup = Time(value=np.array([15.0]), unit=TimeUnit.MIN)
run = Time(value=np.array([45.0]), unit=TimeUnit.MIN)
total = warmup + run

print(total.second)  # [3600.]
print(total.hour)  # [1.]
```
