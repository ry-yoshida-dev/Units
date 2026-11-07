# length

## Overview

This module provides utilities for working with length values and units, including unit conversion and length calculations. A unit and a `MetricPrefix` are given separately, so a kilometer is `M` with `KILO`. Only the meter takes a prefix.

## Components

| Component | Description |
|-----------|-------------|
| [unit.py](./unit.py) | Enum defining length units without prefixes (m, inch, ft, yd, mi, nmi, sun, shaku, ken, ri) with conversion to meters. |
| [length.py](./length.py) | Container class for length values with a unit, a prefix and unit conversion. |

## Examples

```python
import numpy as np

from units import Length, LengthUnit, MetricPrefix

road = Length(value=np.array([2.5]), unit=LengthUnit.M, prefix=MetricPrefix.KILO)
print(road.meter)  # [2500.]

segment = Length(value=np.array([300.0]), unit=LengthUnit.M)
total = road + segment
print(total.km)  # [2.8]
```
