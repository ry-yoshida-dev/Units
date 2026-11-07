from typing_extensions import override

from ..unit import LinearUnit


class VolumeUnit(LinearUnit):
    """
    Enum defining the volume unit, without any prefix.

    Prefixes are given separately as a `MetricPrefix`, so a cubic centimeter is the
    cubic meter with centi, and a milliliter is the liter with milli.

    Attributes
    ----------
    CUBIC_METER: VolumeUnit
        The cubic meter, a cube of one meter.
    LITER: VolumeUnit
        The liter, 10^-3 cubic meters.
    CUBIC_FOOT: VolumeUnit
        The cubic foot, a cube of one foot. It takes no prefix.
    US_GALLON: VolumeUnit
        The US liquid gallon, 3.785411784 liters. It takes no prefix.
    IMPERIAL_GALLON: VolumeUnit
        The imperial gallon, 4.54609 liters. It takes no prefix.
    GO: VolumeUnit
        The go, 1/10 of a sho. It takes no prefix.
    SHO: VolumeUnit
        The sho, 2401/1331 liters. It takes no prefix.
    """

    CUBIC_METER = "m3"
    LITER = "L"
    CUBIC_FOOT = "ft3"
    US_GALLON = "gal"
    IMPERIAL_GALLON = "imp gal"
    GO = "go"
    SHO = "sho"

    @property
    @override
    def factor(self) -> float:
        """
        Return the number of cubic meters in one of this unit, without a prefix.

        Returns
        -------
        float
            The conversion factor to cubic meters.
        """
        match self:
            case VolumeUnit.CUBIC_METER:
                return 1
            case VolumeUnit.LITER:
                return 1e-3
            case VolumeUnit.CUBIC_FOOT:
                return 0.028316846592
            case VolumeUnit.US_GALLON:
                return 3.785411784e-3
            case VolumeUnit.IMPERIAL_GALLON:
                return 4.54609e-3
            case VolumeUnit.GO:
                return 2401 / 13310000
            case VolumeUnit.SHO:
                return 2401 / 1331000

    @property
    @override
    def prefix_power(self) -> int:
        """
        Return the power a prefix is raised to when scaling this unit.

        Returns
        -------
        int
            3 for the cubic meter, whose prefix scales its side, and 1 otherwise.
        """
        return 3 if self is VolumeUnit.CUBIC_METER else 1

    @property
    @override
    def is_prefixable(self) -> bool:
        """
        Return whether this unit takes an SI prefix.

        Returns
        -------
        bool
            True only for the cubic meter and the liter.
        """
        return self in (VolumeUnit.CUBIC_METER, VolumeUnit.LITER)
