# temperature

## Overview

This module provides utilities for working with absolute temperatures and units, including unit conversion. Temperature units differ by an offset as well as a factor, so a temperature has no sum or scalar product. Subtracting two temperatures returns their difference in kelvin as a plain array. Values below absolute zero are rejected.

## Components

| Component | Description |
|-----------|-------------|
| [unit.py](./unit.py) | Enum defining temperature units (K, °C, °F, °R) with the offset and scale of their conversion to kelvin. |
| [temperature.py](./temperature.py) | Container class for absolute temperatures with unit conversion and subtraction. |

## Examples

```python
import numpy as np

from units import Temperature, TemperatureUnit

boiling = Temperature(value=np.array([100.0]), unit=TemperatureUnit.CELSIUS)
print(boiling.kelvin)      # [373.15]
print(boiling.fahrenheit)  # [212.]

freezing = Temperature(value=np.array([32.0]), unit=TemperatureUnit.FAHRENHEIT)
print(boiling - freezing)  # [100.]
```
