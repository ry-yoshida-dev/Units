from ..unit import LinearUnit


class SpeedUnit(LinearUnit):
    """
    Enum defining the speed unit.

    Attributes
    ----------
    METER_PER_SECOND: SpeedUnit
        The meter per second.
    KILOMETER_PER_HOUR: SpeedUnit
        The kilometer per hour.
    MILE_PER_HOUR: SpeedUnit
        The mile per hour.
    FOOT_PER_SECOND: SpeedUnit
        The foot per second.
    KNOT: SpeedUnit
        The knot, one nautical mile per hour.
    """

    METER_PER_SECOND = "m/s"
    KILOMETER_PER_HOUR = "km/h"
    MILE_PER_HOUR = "mph"
    FOOT_PER_SECOND = "ft/s"
    KNOT = "kn"

    @property
    def factor(self) -> float:
        """
        Return the number of meters per second in one of this unit.

        Returns
        -------
        float
            The conversion factor to meters per second.
        """
        match self:
            case SpeedUnit.METER_PER_SECOND:
                return 1
            case SpeedUnit.KILOMETER_PER_HOUR:
                return 1000 / 3600
            case SpeedUnit.MILE_PER_HOUR:
                return 0.44704
            case SpeedUnit.FOOT_PER_SECOND:
                return 0.3048
            case SpeedUnit.KNOT:
                return 1852 / 3600
