# quantity

## Overview

The physical quantities of the package. The base classes shared by every quantity live at this level, and each sub-directory holds a container class for values and an enum of its units. The base classes hold the value, unit and prefix handling, unit conversion, equality, string representations and arithmetic, so that a quantity only defines its units, its accessors and the arithmetic it has with other quantities.

| Base class | Use for | Examples |
|------------|---------|----------|
| `LinearUnit`, `LinearQuantity` | Units that differ only by a factor, with sums and scalar products. | `Length`, `Mass`, `Pressure` |
| `Unit`, `Quantity` | Anything else, such as units with an offset or logarithmic scales. | `Temperature`, `SoundPressureLevel` |

Quantities can be combined across sub-directories, such as `Length * Length` giving an `Area` and `Length / Time` giving a `Speed`.

| Operation | Result |
|-----------|--------|
| `Length * Length` | `Area` in square meters |
| `Length * Area`, `Area * Length` | `Volume` in cubic meters |
| `Area / Length` | `Length` in meters |
| `Volume / Area` | `Length` in meters |
| `Volume / Length` | `Area` in square meters |
| `Length / Time` | `Speed` in meters per second |
| `Length / Speed` | `Time` in seconds |
| `Speed * Time`, `Time * Speed` | `Length` in meters |
| `Speed / Frequency` | `Length` in meters (the wavelength) |
| `Speed / Length` | `Frequency` in hertz |
| `Length * Frequency`, `Frequency * Length` | `Speed` in meters per second |
| `Frequency * Time`, `Time * Frequency` | `NumericArray` (the number of cycles) |

Arithmetic between quantities that is not listed here raises `TypeError`.

## Components

| Component | Description |
|-----------|-------------|
| [unit.py](./unit.py) | Base enums for units, with prefix validation, symbols and conversion to and from the base unit. |
| [quantity.py](./quantity.py) | Base containers for values with a unit and a prefix, unit validation and conversion, equality and arithmetic. |
| [length](./length/) | Length values, given as a unit and an SI prefix, and length unit conversion. |
| [area](./area/) | Area values, given as a unit and an SI prefix, and area unit conversion. |
| [volume](./volume/) | Volume values, given as a unit and an SI prefix, and volume unit conversion. |
| [angle](./angle/) | Angle values, angle unit conversion, and trigonometric operations. |
| [time](./time/) | Durations, given as a unit and an SI prefix, and time unit conversion. |
| [speed](./speed/) | Speed values and speed unit conversion. |
| [mass](./mass/) | Mass values, given as a unit and an SI prefix, and mass unit conversion. |
| [temperature](./temperature/) | Absolute temperatures and temperature unit conversion. |
| [frequency](./frequency/) | Frequency values, given as a unit and an SI prefix, and frequency unit conversion. |
| [pressure](./pressure/) | Pressure values, given as a unit and an SI prefix, and pressure unit conversion. |
| [sound_pressure_level](./sound_pressure_level/) | Sound pressure levels in decibels and their conversion to and from pressure. |

## Adding a quantity

1. Create a sub-directory here with a `README.md`, an `__init__.py`, a `unit.py` and a container module.
2. In `unit.py`, subclass `LinearUnit` and define the members and `factor`. Its base unit must have a factor of 1, and must be the SI-coherent unit if the quantity combines with others. Override `is_prefixable` for units that take a prefix.
3. In the container module, subclass `LinearQuantity` with `base_unit` and, if values cannot be negative, `is_signed=False`. Add a property for each unit worth naming.
4. For a unit that is not a plain factor, subclass `Unit` and `Quantity` instead, and define `to_base` and `from_base`.
5. Export the quantity and its unit from this directory's `__init__.py` and the package `__init__.py`. The tests in `tests/quantity/test_quantity.py` then cover it automatically.
6. For arithmetic with other quantities, override `__mul__` or `__truediv__`, handle those quantities, and pass everything else to `super()`. List the overloads with the scalar first and `Any` last, as the base class does, and import other quantities inside the method if they refer back to this one.
