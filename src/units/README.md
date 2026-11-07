# units

## Overview

This package provides utilities for working with physical quantities and units. SI prefixes, such as kilo and hecto, are kept apart from the units they scale, and `MetricPrefix.NONE` stands for the unit itself.

## Components

| Component | Description |
|-----------|-------------|
| [types.py](./types.py) | Shared NumPy array type aliases for numeric physical quantity values. |
| [prefix.py](./prefix.py) | Enum defining the SI prefixes from peta to femto, plus `NONE` for no prefix, and their factors. |
| [quantity](./quantity/) | Physical quantities, each with a container class and a unit enum. |

## Examples

```python
import numpy as np

from units import Length, LengthUnit, MetricPrefix, Time, TimeUnit

distance = Length(value=np.array([1.2]), unit=LengthUnit.M, prefix=MetricPrefix.KILO)
duration = Time(value=np.array([2.0]), unit=TimeUnit.HR)
print((distance / duration).kilometer_per_hour)  # [0.6]

print(MetricPrefix.KILO.factor)  # 1000.0
print(MetricPrefix.HECTO.value)  # h
```
