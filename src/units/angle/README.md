# angle

## Overview

This module provides utilities for working with angles, including unit conversion between degrees, arcminutes, arcseconds and radians, and trigonometric function calculations.

## Components

| Component | Description |
|-----------|-------------|
| [angle.py](./angle.py) | Container class for angles with unit conversion, conversion to and from degrees-minutes-seconds, and trigonometric operations (sin, cos, tan). |
| [degrees_minutes_seconds.py](./degrees_minutes_seconds.py) | Validated signed sexagesimal (degrees, minutes, seconds) value with carrying normalization. |
| [unit.py](./unit.py) | Enum defining angle units (degree, arcminute, arcsecond, radian) with conversion to degrees. |

## Usage

```python
import numpy as np

from units import Angle, AngleUnit, DegreesMinutesSeconds

theta = Angle(value=np.array([30.0, 45.0, 60.0]), unit=AngleUnit.DEGREE)
print(theta.radian)
print(theta.sin)

theta.convert_unit(AngleUnit.RADIAN)
print(theta.value)

southern_latitude = Angle.from_degrees_minutes_seconds(
    DegreesMinutesSeconds(
        degrees=np.array([35.0]),
        minutes=np.array([40.0]),
        seconds=np.array([30.36]),
        is_negative=np.array([True]),
    )
)
print(southern_latitude.degree)  # [-35.6751]

sexagesimal = Angle(value=np.array([-0.5]), unit=AngleUnit.DEGREE).degrees_minutes_seconds
print(sexagesimal.degrees, sexagesimal.minutes, sexagesimal.is_negative)  # [0.] [30.] [ True]

carried = DegreesMinutesSeconds.normalized(
    degrees=np.array([1.5]),
    minutes=np.array([75.0]),
    seconds=np.array([90.0]),
)
print(carried.degrees, carried.minutes, carried.seconds)  # [2.] [46.] [30.]
```
