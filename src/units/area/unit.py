from enum import Enum

from ..prefix import MetricPrefix


class AreaUnit(Enum):
    """
    Enum defining the area unit, without any prefix.

    Prefixes are given separately as a `MetricPrefix`, so a square kilometer is the
    square meter with kilo, and a hectare is the are with hecto.

    Attributes
    ----------
    SQUARE_METER: AreaUnit
        The square meter, a square of one meter.
    ARE: AreaUnit
        The are, 100 square meters.
    TSUBO: AreaUnit
        The tsubo, 400/121 square meters by the Measurement Act, used for land and
        floor areas in Japan. It takes no prefix.
    """

    SQUARE_METER = "m2"
    ARE = "a"
    TSUBO = "tsubo"

    @property
    def to_square_meter(self) -> float:
        """
        Return the number of square meters in one of this unit, without a prefix.

        Returns
        -------
        float
            The conversion factor to square meters.
        """
        match self:
            case AreaUnit.SQUARE_METER:
                return 1
            case AreaUnit.ARE:
                return 100
            case AreaUnit.TSUBO:
                return 400 / 121

    @property
    def prefix_power(self) -> int:
        """
        Return the power a prefix is raised to when scaling this unit.

        Returns
        -------
        int
            2 for the square meter, whose prefix scales its side, and 1 for the are,
            whose prefix scales the unit itself.
        """
        match self:
            case AreaUnit.SQUARE_METER:
                return 2
            case AreaUnit.ARE | AreaUnit.TSUBO:
                return 1

    @property
    def is_prefixable(self) -> bool:
        """
        Return whether this unit takes an SI prefix.

        Returns
        -------
        bool
            False for units outside the metric system, such as the tsubo.
        """
        match self:
            case AreaUnit.SQUARE_METER | AreaUnit.ARE:
                return True
            case AreaUnit.TSUBO:
                return False

    def validate_prefix(self, prefix: MetricPrefix) -> None:
        """
        Check that this unit takes a prefix.

        Parameters
        ----------
        prefix: MetricPrefix
            The prefix, or `MetricPrefix.NONE` for the unit itself.

        Raises
        ------
        ValueError
            If a prefix other than `MetricPrefix.NONE` is given to a unit that takes none.
        """
        if prefix is not MetricPrefix.NONE and not self.is_prefixable:
            raise ValueError(f"{self.value} takes no prefix: {prefix.value}")

    def prefixed_to_square_meter(self, prefix: MetricPrefix) -> float:
        """
        Return the number of square meters in one of this unit with a prefix.

        Parameters
        ----------
        prefix: MetricPrefix
            The prefix, or `MetricPrefix.NONE` for the unit itself.

        Returns
        -------
        float
            Ten to the prefix exponent times `prefix_power`, times `to_square_meter`.

        Raises
        ------
        ValueError
            If a prefix other than `MetricPrefix.NONE` is given to a unit that takes none.
        """
        self.validate_prefix(prefix)
        return 10.0 ** (prefix.exponent * self.prefix_power) * self.to_square_meter

    def symbol(self, prefix: MetricPrefix) -> str:
        """
        Return the symbol of this unit with a prefix.

        Parameters
        ----------
        prefix: MetricPrefix
            The prefix, or `MetricPrefix.NONE` for the unit itself.

        Returns
        -------
        str
            The symbol, such as `km2` or `ha`.
        """
        return prefix.value + self.value
