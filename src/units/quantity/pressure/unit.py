from typing_extensions import override

from ..unit import LinearUnit


class PressureUnit(LinearUnit):
    """
    Enum defining the pressure unit, without any prefix.

    Prefixes are given separately as a `MetricPrefix`, so a hectopascal is the pascal
    with hecto, and a millibar is the bar with milli. Only the pascal and the bar take a
    prefix.

    Attributes
    ----------
    PASCAL: PressureUnit
        The pascal.
    BAR: PressureUnit
        The bar, 10^5 pascals.
    ATMOSPHERE: PressureUnit
        The standard atmosphere, 101325 pascals.
    TORR: PressureUnit
        The torr, 1/760 of a standard atmosphere.
    MILLIMETER_OF_MERCURY: PressureUnit
        The conventional millimeter of mercury, 133.322387415 pascals.
    KILOGRAM_FORCE_PER_SQUARE_CENTIMETER: PressureUnit
        The kilogram-force per square centimeter, 98066.5 pascals.
    POUND_PER_SQUARE_INCH: PressureUnit
        The pound-force per square inch.
    """

    PASCAL = "Pa"
    BAR = "bar"
    ATMOSPHERE = "atm"
    TORR = "Torr"
    MILLIMETER_OF_MERCURY = "mmHg"
    KILOGRAM_FORCE_PER_SQUARE_CENTIMETER = "kgf/cm2"
    POUND_PER_SQUARE_INCH = "psi"

    @property
    @override
    def factor(self) -> float:
        """
        Return the number of pascals in one of this unit, without a prefix.

        Returns
        -------
        float
            The conversion factor to pascals.
        """
        match self:
            case PressureUnit.PASCAL:
                return 1
            case PressureUnit.BAR:
                return 1e5
            case PressureUnit.ATMOSPHERE:
                return 101325
            case PressureUnit.TORR:
                return 101325 / 760
            case PressureUnit.MILLIMETER_OF_MERCURY:
                return 133.322387415
            case PressureUnit.KILOGRAM_FORCE_PER_SQUARE_CENTIMETER:
                return 98066.5
            case PressureUnit.POUND_PER_SQUARE_INCH:
                return 0.45359237 * 9.80665 / 0.0254**2

    @property
    @override
    def is_prefixable(self) -> bool:
        """
        Return whether this unit takes an SI prefix.

        Returns
        -------
        bool
            True only for the pascal and the bar.
        """
        return self in (PressureUnit.PASCAL, PressureUnit.BAR)
