from enum import Enum


class MetricPrefix(Enum):
    """
    Enum defining the SI prefixes that scale a unit by a power of ten.

    A prefix is not a unit: it scales whichever unit it is attached to. For a unit
    that is a power of a length, such as the square meter, the prefix scales the
    length before it is raised, so a square kilometer is (10^3 m)^2 = 10^6 m^2.

    Attributes
    ----------
    GIGA: MetricPrefix
        10^9, written G.
    MEGA: MetricPrefix
        10^6, written M.
    KILO: MetricPrefix
        10^3, written k.
    HECTO: MetricPrefix
        10^2, written h.
    DECA: MetricPrefix
        10^1, written da.
    NONE: MetricPrefix
        10^0, written as nothing, for the unit itself.
    DECI: MetricPrefix
        10^-1, written d.
    CENTI: MetricPrefix
        10^-2, written c.
    MILLI: MetricPrefix
        10^-3, written m.
    MICRO: MetricPrefix
        10^-6, written µ.
    NANO: MetricPrefix
        10^-9, written n.
    """

    GIGA = "G"
    MEGA = "M"
    KILO = "k"
    HECTO = "h"
    DECA = "da"
    NONE = ""
    DECI = "d"
    CENTI = "c"
    MILLI = "m"
    MICRO = "µ"
    NANO = "n"

    @property
    def exponent(self) -> int:
        """
        Return the power of ten this prefix stands for.

        Returns
        -------
        int
            The exponent, such as 3 for kilo.
        """
        match self:
            case MetricPrefix.GIGA:
                return 9
            case MetricPrefix.MEGA:
                return 6
            case MetricPrefix.KILO:
                return 3
            case MetricPrefix.HECTO:
                return 2
            case MetricPrefix.DECA:
                return 1
            case MetricPrefix.NONE:
                return 0
            case MetricPrefix.DECI:
                return -1
            case MetricPrefix.CENTI:
                return -2
            case MetricPrefix.MILLI:
                return -3
            case MetricPrefix.MICRO:
                return -6
            case MetricPrefix.NANO:
                return -9

    @property
    def factor(self) -> float:
        """
        Return the factor this prefix scales a unit by.

        Returns
        -------
        float
            Ten to the power of `exponent`, such as 1000 for kilo.
        """
        return 10.0**self.exponent
