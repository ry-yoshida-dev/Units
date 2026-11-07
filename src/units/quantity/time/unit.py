from typing_extensions import override

from ..unit import LinearUnit


class TimeUnit(LinearUnit):
    """
    Enum defining the time unit, without any prefix.

    Prefixes are given separately as a `MetricPrefix`, so a millisecond is the second
    with milli. Only the second takes a prefix.

    Attributes
    ----------
    S: TimeUnit
        The second.
    MIN: TimeUnit
        The minute.
    HR: TimeUnit
        The hour.
    DAY: TimeUnit
        The day, 24 hours.
    WEEK: TimeUnit
        The week, 7 days.
    """

    S = "s"
    MIN = "min"
    HR = "h"
    DAY = "day"
    WEEK = "week"

    @property
    @override
    def factor(self) -> float:
        """
        Return the number of seconds in one of this unit, without a prefix.

        Returns
        -------
        float
            The conversion factor to seconds.
        """
        match self:
            case TimeUnit.S:
                return 1.0
            case TimeUnit.MIN:
                return 60.0
            case TimeUnit.HR:
                return 3600.0
            case TimeUnit.DAY:
                return 86400.0
            case TimeUnit.WEEK:
                return 604800.0

    @property
    @override
    def is_prefixable(self) -> bool:
        """
        Return whether this unit takes an SI prefix.

        Returns
        -------
        bool
            True only for the second.
        """
        return self is TimeUnit.S
