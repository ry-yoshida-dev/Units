# mass

## Overview

This module provides utilities for working with mass values and units, including unit conversion. A unit and a `MetricPrefix` are given separately, so a kilogram is `GRAM` with `KILO`. Only the gram and the tonne take a prefix.

## Components

| Component | Description |
|-----------|-------------|
| [unit.py](./unit.py) | Enum defining mass units without prefixes (g, t, lb, oz, ct, momme, kin, kan) and their conversion to grams. |
| [mass.py](./mass.py) | Container class for mass values with a unit, a prefix and unit conversion. |

## Examples

```python
import numpy as np

from units import Mass, MassUnit, MetricPrefix

parcel = Mass(value=np.array([2.5]), unit=MassUnit.GRAM, prefix=MetricPrefix.KILO)
print(parcel.gram)  # [2500.]
print(parcel.tonne)  # [0.0025]
print(parcel)  # [2.5] kg
```
