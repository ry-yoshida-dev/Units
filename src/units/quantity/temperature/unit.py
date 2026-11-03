from ...prefix import MetricPrefix
from ...types import NumericArray, as_numeric_array
from ..base import Unit


class TemperatureUnit(Unit):
    """
    Enum defining the temperature unit.

    Unlike other units, these differ by an offset as well as a factor, so a value is
    converted to kelvin as (value + `offset_to_absolute`) * `to_kelvin_scale`.

    Attributes
    ----------
    KELVIN: TemperatureUnit
        The kelvin.
    CELSIUS: TemperatureUnit
        The degree Celsius.
    FAHRENHEIT: TemperatureUnit
        The degree Fahrenheit.
    RANKINE: TemperatureUnit
        The degree Rankine.
    """

    KELVIN = "K"
    CELSIUS = "°C"
    FAHRENHEIT = "°F"
    RANKINE = "°R"

    @property
    def offset_to_absolute(self) -> float:
        """
        Return the value of this unit's zero above absolute zero, in this unit.

        Returns
        -------
        float
            The offset added to a value before it is scaled to kelvin.
        """
        match self:
            case TemperatureUnit.KELVIN | TemperatureUnit.RANKINE:
                return 0.0
            case TemperatureUnit.CELSIUS:
                return 273.15
            case TemperatureUnit.FAHRENHEIT:
                return 459.67

    @property
    def to_kelvin_scale(self) -> float:
        """
        Return the size of one degree of this unit in kelvin.

        Returns
        -------
        float
            The factor from an absolute value in this unit to kelvin.
        """
        match self:
            case TemperatureUnit.KELVIN | TemperatureUnit.CELSIUS:
                return 1.0
            case TemperatureUnit.FAHRENHEIT | TemperatureUnit.RANKINE:
                return 5.0 / 9.0

    def to_base(self, value: NumericArray, prefix: MetricPrefix = MetricPrefix.NONE) -> NumericArray:
        self.validate_prefix(prefix)
        return as_numeric_array((value + self.offset_to_absolute) * self.to_kelvin_scale)

    def from_base(self, value: NumericArray, prefix: MetricPrefix = MetricPrefix.NONE) -> NumericArray:
        self.validate_prefix(prefix)
        return as_numeric_array(value / self.to_kelvin_scale - self.offset_to_absolute)
