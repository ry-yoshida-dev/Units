# Units

## Overview
`units` is a Python package for working with physical quantities and unit conversion.
It provides utilities for **length**, **area**, **volume**, **angle**, **time**, **speed**, **mass**, **temperature**, **frequency**, **pressure**, and **sound pressure level** values with simple arithmetic and conversion helpers.
See [src/units/README.md](src/units/README.md) for package details.

## Installation

From the project root:

```bash
pip install -e .
```

## Usage

```python
import numpy as np
from units import Angle, AngleUnit, Length, LengthUnit, MetricPrefix, Time, TimeUnit

l1 = Length(value=np.array([1.0, 2.0]), unit=LengthUnit.M)
l2 = Length(value=np.array([50.0, 50.0]), unit=LengthUnit.M, prefix=MetricPrefix.CENTI)
total = l1 + l2
print(total.meter)  # [1.5, 2.5]

a = Angle(value=np.array([0.0, 90.0]), unit=AngleUnit.DEGREE)
print(a.radian)  # [0.0, 1.57079633...]
print(a.sin)     # [0.0, 1.0]

t = Time(value=np.array([1.0, 0.5]), unit=TimeUnit.HR)
print(t.second)  # [3600.0, 1800.0]
```
