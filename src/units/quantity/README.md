# quantity

## Overview

The physical quantities of the package. Each sub-directory holds a container class for values and an enum of its units. Quantities can be combined across sub-directories, such as `Length * Length` giving an `Area` and `Length / Time` giving a `Speed`.

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
| [base](./base/) | Base classes shared by every quantity. |
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
5. Export the quantity and its unit from this directory's `__init__.py` and the package `__init__.py`. The tests in `tests/quantity/base` then cover it automatically.
6. For arithmetic with other quantities, override `__mul__` or `__truediv__`, handle those quantities, and pass everything else to `super()`. List the overloads with the scalar first and `Any` last, as the base class does, and import other quantities inside the method if they refer back to this one.
