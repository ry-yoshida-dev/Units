# base

## Overview

Base classes shared by every quantity. They hold the value, unit and prefix handling, unit conversion, equality, string representations and arithmetic, so that a quantity only defines its units, its accessors and the arithmetic it has with other quantities.

| Base class | Use for | Examples |
|------------|---------|----------|
| `LinearUnit`, `LinearQuantity` | Units that differ only by a factor, with sums and scalar products. | `Length`, `Mass`, `Pressure` |
| `Unit`, `Quantity` | Anything else, such as units with an offset or logarithmic scales. | `Temperature`, `SoundPressureLevel` |

## Components

| Component | Description |
|-----------|-------------|
| [unit.py](./unit.py) | Base enums for units, with prefix validation, symbols and conversion to and from the base unit. |
| [quantity.py](./quantity.py) | Base containers for values with a unit and a prefix, unit validation and conversion, equality and arithmetic. |
