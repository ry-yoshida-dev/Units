# area

## Overview

This module provides utilities for working with area values and units, such as the hectares of a
land parcel or the square kilometers of an administrative area, including unit conversion.

Unlike `LengthUnit`, whose members such as `KM` bake a prefix into the unit, an area is given a
unit and a `MetricPrefix` separately. The prefix scales the unit raised to its `prefix_power`: it
scales the side of a square meter, so a square kilometer is 10^6 square meters, and the are
itself, so a hectare is 10^2 ares. Units outside the metric system, such as the tsubo, take no
prefix other than `MetricPrefix.NONE`.

| Area | Unit | Prefix | Square meters |
|------|------|--------|---------------|
| km² | `SQUARE_METER` | `KILO` | (10^3)^2 = 10^6 |
| m² | `SQUARE_METER` | `NONE` | 1 |
| ha | `ARE` | `HECTO` | 10^2 × 100 = 10^4 |
| a | `ARE` | `NONE` | 100 |
| 坪 | `TSUBO` | `NONE` | 400/121 |

## Components

| Component | Description |
|-----------|-------------|
| [unit.py](./unit.py) | Enum defining area units without prefixes (m², a, tsubo), their conversion to square meters and the power a prefix is raised to. |
| [area.py](./area.py) | Container class for area values with a unit, a prefix and unit conversion. |

## Usage

```python
import numpy as np

from units import Area, AreaUnit, MetricPrefix

parcel = Area(value=np.array([2500.0]), unit=AreaUnit.SQUARE_METER)
print(parcel.hectare)  # [0.25]

parcel.convert_unit(AreaUnit.ARE, MetricPrefix.HECTO)
print(parcel)  # [0.25] ha

city = Area(value=np.array([21.58]), unit=AreaUnit.SQUARE_METER, prefix=MetricPrefix.KILO)
print(city.hectare)  # [2158.]
```
