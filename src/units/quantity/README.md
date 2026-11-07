# quantity

## Overview

The physical quantities of the package. The base classes shared by every quantity live at this level, and each sub-directory holds a container class for values and an enum of its units. Quantities can be combined across sub-directories, such as `Length * Length` giving an `Area` and `Length / Time` giving a `Speed`. See [docs/quantities.md](../../../docs/quantities.md) for the supported arithmetic between quantities.

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
