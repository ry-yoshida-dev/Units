"""Shared NumPy array type aliases for physical quantity values."""

from typing import TypeAlias, cast

import numpy as np
from numpy.typing import NDArray

NumericArray: TypeAlias = NDArray[np.integer | np.floating]


def as_numeric_array(array: NDArray[np.number]) -> NumericArray:
    """Narrow a NumPy numeric array to integer or floating dtype."""
    return cast(NumericArray, array)
