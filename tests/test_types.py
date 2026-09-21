from __future__ import annotations

import numpy as np

from units import NumericArray
from units.types import as_numeric_array


def test_as_numeric_array_returns_same_array() -> None:
    array: NumericArray = np.array([1.0, 2.0])
    assert as_numeric_array(array) is array


def test_as_numeric_array_keeps_integer_dtype() -> None:
    array: NumericArray = np.array([1, 2])
    assert as_numeric_array(array).dtype == array.dtype
