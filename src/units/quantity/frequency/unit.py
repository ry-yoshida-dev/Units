from ..base import LinearUnit


class FrequencyUnit(LinearUnit):
    """
    Enum defining the frequency unit, without any prefix.

    Prefixes are given separately as a `MetricPrefix`, so a kilohertz is the hertz with
    kilo. Only the hertz takes a prefix.

    Attributes
    ----------
    HERTZ: FrequencyUnit
        The hertz, one cycle per second.
    RPM: FrequencyUnit
        The revolution per minute.
    BPM: FrequencyUnit
        The beat per minute.
    """

    HERTZ = "Hz"
    RPM = "rpm"
    BPM = "bpm"

    @property
    def factor(self) -> float:
        """
        Return the number of hertz in one of this unit, without a prefix.

        Returns
        -------
        float
            The conversion factor to hertz.
        """
        match self:
            case FrequencyUnit.HERTZ:
                return 1
            case FrequencyUnit.RPM | FrequencyUnit.BPM:
                return 1 / 60

    @property
    def is_prefixable(self) -> bool:
        """
        Return whether this unit takes an SI prefix.

        Returns
        -------
        bool
            True only for the hertz.
        """
        return self is FrequencyUnit.HERTZ
