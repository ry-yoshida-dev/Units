# quantity

## Overview

Tests for the `units.quantity` package. Each sub-directory covers one quantity, and arithmetic that crosses quantities is tested at this level.

## Components

| Component | Description |
|-----------|-------------|
| [length](./length/) | Tests for `Length` and `LengthUnit`. |
| [area](./area/) | Tests for `Area` and `AreaUnit`. |
| [volume](./volume/) | Tests for `Volume` and `VolumeUnit`. |
| [angle](./angle/) | Tests for `Angle`, `AngleUnit` and `DegreesMinutesSeconds`. |
| [time](./time/) | Tests for `Time` and `TimeUnit`. |
| [speed](./speed/) | Tests for `Speed` and `SpeedUnit`. |
| [mass](./mass/) | Tests for `Mass` and `MassUnit`. |
| [temperature](./temperature/) | Tests for `Temperature` and `TemperatureUnit`. |
| [frequency](./frequency/) | Tests for `Frequency` and `FrequencyUnit`. |
| [pressure](./pressure/) | Tests for `Pressure` and `PressureUnit`. |
| [sound_pressure_level](./sound_pressure_level/) | Tests for `SoundPressureLevel` and `SoundPressureLevelUnit`. |
| [test_quantity.py](./test_quantity.py) | Contract tests applied to every `Quantity` subclass, so a new quantity is covered by them automatically. |
| [test_operations.py](./test_operations.py) | Tests for arithmetic that crosses quantities, such as `Length * Length` and `Length / Time`, and for rejecting arithmetic between unrelated quantities. |
