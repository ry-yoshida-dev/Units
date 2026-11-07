# volume

## Overview

This module provides utilities for working with volume values and units, including unit conversion. A unit and a `MetricPrefix` are given separately. The prefix scales the side of a cubic meter, so a cubic centimeter is 10^-6 cubic meters, and the liter itself, so a milliliter is 10^-3 liters. Units outside the metric system take no prefix.

## Components

| Component | Description |
|-----------|-------------|
| [unit.py](./unit.py) | Enum defining volume units without prefixes (m³, L, ft³, gal, imp gal, go, sho), their conversion to cubic meters and the power a prefix is raised to. |
| [volume.py](./volume.py) | Container class for volume values with a unit, a prefix and unit conversion. |

## Examples

```python
import numpy as np

from units import MetricPrefix, Volume, VolumeUnit

tank = Volume(value=np.array([2.0]), unit=VolumeUnit.CUBIC_METER)
print(tank.liter)  # [2000.]

dose = Volume(value=np.array([250.0]), unit=VolumeUnit.LITER, prefix=MetricPrefix.MILLI)
print(dose)  # [250.] mL
```
