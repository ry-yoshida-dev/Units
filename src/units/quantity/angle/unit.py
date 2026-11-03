import math

from ..base import LinearUnit

class AngleUnit(LinearUnit):
    """
    Enum defining the angle unit.

    Attributes
    ----------
    DEGREE: AngleUnit
        The angle unit is degree.
    ARCMINUTE: AngleUnit
        The angle unit is arcminute, 1/60 of a degree.
    ARCSECOND: AngleUnit
        The angle unit is arcsecond, 1/60 of an arcminute.
    RADIAN: AngleUnit
        The angle unit is radian.
    GRADIAN: AngleUnit
        The angle unit is gradian, 1/400 of a turn.
    TURN: AngleUnit
        The angle unit is turn, a full revolution of 360 degrees.
    """
    DEGREE = "degree"
    ARCMINUTE = "arcminute"
    ARCSECOND = "arcsecond"
    RADIAN = "radian"
    GRADIAN = "gradian"
    TURN = "turn"

    @property
    def factor(self) -> float:
        """
        Return the number of degrees in one unit.

        Returns
        -------
        float
            The conversion factor from this unit to degrees.
        """
        match self:
            case AngleUnit.DEGREE:
                return 1.0
            case AngleUnit.ARCMINUTE:
                return 1.0 / 60.0
            case AngleUnit.ARCSECOND:
                return 1.0 / 3600.0
            case AngleUnit.RADIAN:
                return math.degrees(1.0)
            case AngleUnit.GRADIAN:
                return 0.9
            case AngleUnit.TURN:
                return 360.0

    @property
    def as_upper(self) -> str:
        return str(self.value).upper()

    @property
    def as_lower(self) -> str:
        return str(self.value).lower()

    @property
    def is_degree(self) -> bool:
        return self is AngleUnit.DEGREE

    @property
    def is_radian(self) -> bool:
        return self is AngleUnit.RADIAN
