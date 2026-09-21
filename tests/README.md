# tests

## Overview

Pytest suite covering unit conversion, validation, arithmetic and equality for every quantity in the `units` package.

## Components

| Component | Description |
|-----------|-------------|
| [test_angle.py](./test_angle.py) | Tests for `Angle` and `AngleUnit`, including unit conversion, degrees-minutes-seconds round trips, negation and trigonometry. |
| [test_degrees_minutes_seconds.py](./test_degrees_minutes_seconds.py) | Tests for `DegreesMinutesSeconds` validation, sign handling, carrying normalization and equality. |
| [test_length.py](./test_length.py) | Tests for `Length` and `LengthUnit`, including non-negativity validation. |
| [test_time.py](./test_time.py) | Tests for `Time` and `TimeUnit`. |
| [test_types.py](./test_types.py) | Tests for the shared numeric array helpers. |

## Examples

```bash
pip install -e ".[dev]"
pytest
```
