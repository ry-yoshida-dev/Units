"""Shared NumPy array type aliases for physical quantity values."""

from typing import Any, TypeAlias, cast

import numpy as np
from numpy.typing import NDArray

NumericArray: TypeAlias = NDArray[np.integer[Any] | np.floating[Any]]


def as_numeric_array(array: NDArray[np.number[Any]]) -> NumericArray:
    """Narrow a NumPy numeric array to integer or floating dtype."""
    return cast(NumericArray, array)
