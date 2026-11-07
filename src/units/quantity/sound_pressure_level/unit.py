from typing_extensions import override

from ..unit import LinearUnit


class SoundPressureLevelUnit(LinearUnit):
    """
    Enum defining the unit of a sound pressure level.

    Attributes
    ----------
    DECIBEL: SoundPressureLevelUnit
        The decibel.
    BEL: SoundPressureLevelUnit
        The bel, 10 decibels.
    """

    DECIBEL = "dB"
    BEL = "B"

    @property
    @override
    def factor(self) -> float:
        """
        Return the number of decibels in one of this unit.

        Returns
        -------
        float
            The conversion factor to decibels.
        """
        match self:
            case SoundPressureLevelUnit.DECIBEL:
                return 1
            case SoundPressureLevelUnit.BEL:
                return 10
