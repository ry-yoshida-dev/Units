# prefix

## Overview

SI prefixes, such as kilo and hecto, kept apart from the units they scale. A prefix
applies to the length of a unit before the unit is raised to its power, so kilo makes a
square meter 10^6 times larger and an are only 10^3 times. `MetricPrefix.NONE` stands for
the unit itself.

## Components

| Component | Description |
|-----------|-------------|
| [metric_prefix.py](./metric_prefix.py) | Enum defining the SI prefixes from giga to nano, plus `NONE` for no prefix, and their factors. |

## Usage

```python
from units import MetricPrefix

print(MetricPrefix.KILO.factor)  # 1000.0
print(MetricPrefix.HECTO.value)  # h
```
