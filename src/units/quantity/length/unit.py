from ..unit import LinearUnit


class LengthUnit(LinearUnit):
    """
    Enum defining the length unit, without any prefix.

    Prefixes are given separately as a `MetricPrefix`, so a kilometer is the meter
    with kilo. Only the meter takes a prefix.

    Attributes
    ----------
    M: LengthUnit
        The meter.
    INCH: LengthUnit
        The inch, 25.4 millimeters.
    FOOT: LengthUnit
        The foot, 12 inches.
    YARD: LengthUnit
        The yard, 3 feet.
    MILE: LengthUnit
        The mile, 1760 yards.
    NAUTICAL_MILE: LengthUnit
        The nautical mile, 1852 meters.
    SUN: LengthUnit
        The sun, 1/10 of a shaku.
    SHAKU: LengthUnit
        The shaku, 10/33 meters by the Measurement Act of Japan.
    KEN: LengthUnit
        The ken, 6 shaku, the side of a square of one tsubo.
    RI: LengthUnit
        The ri, 12960 shaku.
    """

    M = "m"
    INCH = "inch"
    FOOT = "ft"
    YARD = "yd"
    MILE = "mi"
    NAUTICAL_MILE = "nmi"
    SUN = "sun"
    SHAKU = "shaku"
    KEN = "ken"
    RI = "ri"

    @property
    def factor(self) -> float:
        """
        Return the number of meters in one of this unit, without a prefix.

        Returns
        -------
        float
            The conversion factor to meters.
        """
        match self:
            case LengthUnit.M:
                return 1
            case LengthUnit.INCH:
                return 0.0254
            case LengthUnit.FOOT:
                return 0.3048
            case LengthUnit.YARD:
                return 0.9144
            case LengthUnit.MILE:
                return 1609.344
            case LengthUnit.NAUTICAL_MILE:
                return 1852
            case LengthUnit.SUN:
                return 1 / 33
            case LengthUnit.SHAKU:
                return 10 / 33
            case LengthUnit.KEN:
                return 20 / 11
            case LengthUnit.RI:
                return 43200 / 11

    @property
    def is_prefixable(self) -> bool:
        """
        Return whether this unit takes an SI prefix.

        Returns
        -------
        bool
            True only for the meter.
        """
        return self is LengthUnit.M
