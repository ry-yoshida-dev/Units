from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from ..types import NumericArray, as_numeric_array

SEXAGESIMAL_BASE: int = 60
SECONDS_PER_DEGREE: int = SEXAGESIMAL_BASE * SEXAGESIMAL_BASE
EQUALITY_TOLERANCE_SECONDS: float = 1e-6
SECONDS_ROUNDING_DECIMALS: int = 6


@dataclass(frozen=True)
class DegreesMinutesSeconds:
    """
    Signed angle in canonical sexagesimal notation.

    The magnitude is held by non-negative degrees, minutes and seconds, and
    the sign is held separately so that angles such as -0°30' are expressible.

    Parameters
    ----------
    degrees : NumericArray
        The whole degrees of the magnitude.
    minutes : NumericArray
        The whole arcminutes of the magnitude, in the range [0, 60).
    seconds : NumericArray
        The arcseconds of the magnitude, in the range [0, 60).
    is_negative : NDArray[np.bool_]
        Whether each angle is negative, such as a southern latitude or a
        western longitude.

    Raises
    ------
    TypeError
        If ``is_negative`` is not a boolean array.
    ValueError
        If the components are not 1D arrays of the same shape, if any
        magnitude component is negative, if degrees or minutes are not whole
        numbers, or if any minute or second is 60 or greater. Use
        ``normalized`` to carry overflowing or fractional components instead.
    """
    degrees: NumericArray
    minutes: NumericArray
    seconds: NumericArray
    is_negative: NDArray[np.bool_]

    def __post_init__(self) -> None:
        if self.is_negative.dtype != np.bool_:
            raise TypeError("is_negative must be a boolean array")
        if self.degrees.ndim != 1:
            raise ValueError("Degrees, minutes and seconds must be 1D arrays")
        if not self.degrees.shape == self.minutes.shape == self.seconds.shape == self.is_negative.shape:
            raise ValueError("Degrees, minutes, seconds and is_negative must have the same shape")
        if np.any(self.degrees < 0) or np.any(self.minutes < 0) or np.any(self.seconds < 0):
            raise ValueError("Degrees, minutes and seconds must be non-negative")
        if not np.array_equal(np.floor(self.degrees), self.degrees) or not np.array_equal(np.floor(self.minutes), self.minutes):
            raise ValueError("Degrees and minutes must be whole numbers")
        if np.any(self.minutes >= SEXAGESIMAL_BASE) or np.any(self.seconds >= SEXAGESIMAL_BASE):
            raise ValueError("Minutes and seconds must be less than 60")

    @classmethod
    def normalized(
        cls,
        degrees: NumericArray,
        minutes: NumericArray,
        seconds: NumericArray,
        is_negative: NDArray[np.bool_] | None = None,
        ) -> DegreesMinutesSeconds:
        """
        Build a canonical value by carrying overflowing and fractional components.

        The total is rounded to micro-arcseconds before carrying so that
        floating-point noise such as 59.99999999998 seconds carries into the
        next minute instead of being kept as a near-60 second.

        Parameters
        ----------
        degrees : NumericArray
            The degrees of the magnitude, possibly fractional.
        minutes : NumericArray
            The arcminutes of the magnitude, possibly 60 or greater or fractional.
        seconds : NumericArray
            The arcseconds of the magnitude, possibly 60 or greater.
        is_negative : NDArray[np.bool_] | None
            Whether each angle is negative. All angles are non-negative when omitted.

        Returns
        -------
        DegreesMinutesSeconds
            The equivalent value with whole degrees and minutes, and minutes
            and seconds in the range [0, 60).

        Raises
        ------
        ValueError
            If the components differ in shape, or if any magnitude component
            is negative.
        """
        if not degrees.shape == minutes.shape == seconds.shape:
            raise ValueError("Degrees, minutes and seconds must have the same shape")
        if np.any(degrees < 0) or np.any(minutes < 0) or np.any(seconds < 0):
            raise ValueError("Degrees, minutes and seconds must be non-negative")
        total_seconds: NumericArray = as_numeric_array(
            np.round(degrees * SECONDS_PER_DEGREE + minutes * SEXAGESIMAL_BASE + seconds, SECONDS_ROUNDING_DECIMALS)
            )
        whole_degrees: NumericArray = as_numeric_array(np.floor_divide(total_seconds, SECONDS_PER_DEGREE))
        remaining_seconds: NumericArray = as_numeric_array(total_seconds - whole_degrees * SECONDS_PER_DEGREE)
        whole_minutes: NumericArray = as_numeric_array(np.floor_divide(remaining_seconds, SEXAGESIMAL_BASE))
        return cls(
            degrees=whole_degrees,
            minutes=whole_minutes,
            seconds=as_numeric_array(remaining_seconds - whole_minutes * SEXAGESIMAL_BASE),
            is_negative=np.zeros(degrees.shape, dtype=np.bool_) if is_negative is None else is_negative,
            )

    @property
    def total_seconds(self) -> NumericArray:
        """
        Return the signed angle in arcseconds.

        Returns
        -------
        NumericArray
            The signed angle in arcseconds.
        """
        magnitude: NumericArray = as_numeric_array(
            self.degrees * SECONDS_PER_DEGREE + self.minutes * SEXAGESIMAL_BASE + self.seconds
            )
        return as_numeric_array(np.where(self.is_negative, -magnitude, magnitude))

    def __eq__(self, other: object) -> bool:
        """Compare if this angle is equal to another."""
        if not isinstance(other, DegreesMinutesSeconds):
            return False
        return self.degrees.shape == other.degrees.shape and np.allclose(
            self.total_seconds, other.total_seconds, atol=EQUALITY_TOLERANCE_SECONDS
            )

    def __len__(self) -> int:
        """
        Return the number of angles.

        Returns
        -------
        int
            The number of angles.
        """
        return len(self.degrees)
