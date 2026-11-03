# tests

## Overview

Pytest suite for the `units` package. The directories mirror `src/units`, so the tests of `src/units/quantity/length/length.py` live in `quantity/length/test_length.py`. Add new tests next to the mirrored path. Test modules are imported in `importlib` mode, so the same file name may appear in different directories and the directories need no `__init__.py`.

## Components

| Component | Description |
|-----------|-------------|
| [prefix](./prefix/) | Tests for the metric prefixes. |
| [quantity](./quantity/) | Tests for each physical quantity and for arithmetic across quantities. |
| [test_types.py](./test_types.py) | Tests for the shared numeric array helpers. |

## Examples

```bash
pip install -e ".[dev]"
pytest
pytest tests/quantity/length
```
