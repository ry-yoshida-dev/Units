from ..base import LinearUnit


class AreaUnit(LinearUnit):
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
    SQUARE_FOOT: AreaUnit
        The square foot, a square of one foot. It takes no prefix.
    ACRE: AreaUnit
        The international acre, 43560 square feet. It takes no prefix.
    TSUBO: AreaUnit
        The tsubo, 400/121 square meters by the Measurement Act, used for land and
        floor areas in Japan. It takes no prefix.
    JO: AreaUnit
        The jo, 1.62 square meters, the minimum per mat that Japanese real estate
        advertising rules allow. Actual mats vary by region. It takes no prefix.
    SE: AreaUnit
        The se, 30 tsubo. It takes no prefix.
    TAN: AreaUnit
        The tan, 300 tsubo. It takes no prefix.
    CHO: AreaUnit
        The cho, 3000 tsubo. It takes no prefix.
    """

    SQUARE_METER = "m2"
    ARE = "a"
    SQUARE_FOOT = "ft2"
    ACRE = "acre"
    TSUBO = "tsubo"
    JO = "jo"
    SE = "se"
    TAN = "tan"
    CHO = "cho"

    @property
    def factor(self) -> float:
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
            case AreaUnit.SQUARE_FOOT:
                return 0.09290304
            case AreaUnit.ACRE:
                return 4046.8564224
            case AreaUnit.TSUBO:
                return 400 / 121
            case AreaUnit.JO:
                return 1.62
            case AreaUnit.SE:
                return 12000 / 121
            case AreaUnit.TAN:
                return 120000 / 121
            case AreaUnit.CHO:
                return 1200000 / 121

    @property
    def prefix_power(self) -> int:
        """
        Return the power a prefix is raised to when scaling this unit.

        Returns
        -------
        int
            2 for the square meter, whose prefix scales its side, and 1 otherwise.
        """
        return 2 if self is AreaUnit.SQUARE_METER else 1

    @property
    def is_prefixable(self) -> bool:
        """
        Return whether this unit takes an SI prefix.

        Returns
        -------
        bool
            True only for the square meter and the are.
        """
        return self in (AreaUnit.SQUARE_METER, AreaUnit.ARE)
