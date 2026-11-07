from typing_extensions import override

from ..unit import LinearUnit


class MassUnit(LinearUnit):
    """
    Enum defining the mass unit, without any prefix.

    Prefixes are given separately as a `MetricPrefix`, so a kilogram is the gram with
    kilo. Only the gram and the tonne take a prefix.

    Attributes
    ----------
    GRAM: MassUnit
        The gram.
    TONNE: MassUnit
        The metric tonne, 10^6 grams.
    POUND: MassUnit
        The international avoirdupois pound, 453.59237 grams.
    OUNCE: MassUnit
        The avoirdupois ounce, 1/16 of a pound.
    CARAT: MassUnit
        The metric carat, 0.2 grams.
    MOMME: MassUnit
        The momme, 3.75 grams.
    KIN: MassUnit
        The kin, 160 momme.
    KAN: MassUnit
        The kan, 1000 momme.
    """

    GRAM = "g"
    TONNE = "t"
    POUND = "lb"
    OUNCE = "oz"
    CARAT = "ct"
    MOMME = "momme"
    KIN = "kin"
    KAN = "kan"

    @property
    @override
    def factor(self) -> float:
        """
        Return the number of grams in one of this unit, without a prefix.

        Returns
        -------
        float
            The conversion factor to grams.
        """
        match self:
            case MassUnit.GRAM:
                return 1
            case MassUnit.TONNE:
                return 1e6
            case MassUnit.POUND:
                return 453.59237
            case MassUnit.OUNCE:
                return 28.349523125
            case MassUnit.CARAT:
                return 0.2
            case MassUnit.MOMME:
                return 3.75
            case MassUnit.KIN:
                return 600
            case MassUnit.KAN:
                return 3750

    @property
    @override
    def is_prefixable(self) -> bool:
        """
        Return whether this unit takes an SI prefix.

        Returns
        -------
        bool
            True only for the gram and the tonne.
        """
        return self in (MassUnit.GRAM, MassUnit.TONNE)
