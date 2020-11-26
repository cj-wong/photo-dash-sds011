from dataclasses import asdict, dataclass
from typing import Dict, List, Union


@dataclass
class AirQualityRange:
    """Represents a single air quality range given an associated PM size.

    Attributes:
        label (str): the quality label for this range, e.g. Good
        pm (float): either 2.5 or 10 (PM2.5, PM10)
        color (str): a color in the format (hex) RRGGBB
        lower (int): the lower bound, inclusive, for this range
        upper (int): the upper bound, exclusive, for this range;
            if 0, there is no upper bound; defaults to 0

    """

    label: str
    pm: float
    color: str
    lower: int
    upper: int

    DICT_TYPE = Dict[str, Union[str, float]]

    def in_range(self, reading: int) -> bool:
        """Check if a reading fits within the range.

        Args:
            reading (int): an air quality reading

        Returns:
            bool: True if the reading corresponds to this range

        """
        # Special case: no upper bound, only a lower bound
        if self.upper == -1:
            return self.lower <= reading
        else:
            return self.lower <= reading and reading < self.upper


class AirQuality:
    """Generic class for air quality, irrespective of PM size.

    This class should not be used directly. Subclasses should have
    both RANGES and UPPER attributes set and in __init__, call
    self.populate_range_list().

    Attributes:
        _LABELS_COLORS (List[Tuple[str, str]]): a list of labels and
            their colors in hex
        RANGES (List[int]): a list of numeric markers denoting ranges
        UPPER (int): an upper bound; although readings can technically
            exceed this, the resulting image must have an appropriate
            upper bound

    """

    # Colors taken from:
    #   https://www.airnow.gov/themes/anblue/images/dial2/dial_legend.svg
    # Ranges calculated by:
    #   https://www.airnow.gov/aqi/aqi-calculator/
    # Ranges are slightly modified as to be integers.
    # e.g. 12 would have been 'Good', but will now be 'Moderate'.
    # In other words, the upper bound is rounded to the nearest integer and
    # is exclusive.
    _LABELS_COLORS = [
        ('Good', '#00E400'),
        ('Moderate', '#FFFF00'),
        ('Unhealthy for sensitive groups', '#FF6600'),
        ('Unhealthy', '#FF0000'),
        ('Very Unhealthy', '#8F3F97'),
        ('Hazardous', '#660033')
        ]

    def __init__(self) -> None:
        """In the subclasses, set self.size to the appropriate value."""
        pass

    def get_all_colors(self) -> List[str]:
        """Get all the colors on the gauge for air quality.

        Returns:
            List[str]: a list of the colors in hex

        """
        return [color for label, color in self._LABELS_COLORS]

    def get_all_ranges(self) -> List[int]:
        """Get the ranges of air quality given numeric markers.

        Returns:
            List[int]: a list of numeric markers, plus a soft upper bound

        """
        return self.RANGES + [self.UPPER]

    def get_range(self, reading: float) -> AirQualityRange.DICT_TYPE:
        """Get the appropriate AirQuality range given reading and pm.

        Args:
            pm (float): either 2.5 or 10 (PM2.5, PM10)
            reading (float): an air quality reading from the sensor

        Returns:
            AirQualityRange.DICT_TYPE: a dictionary containing the
                range's parameters

        """
        for aqr in self.AQ_RANGES:
            if aqr.in_range(reading):
                return asdict(aqr)

    def populate_range_list(self) -> None:
        """Populate the list of AQ ranges."""
        try:
            if self.AQ_RANGES:
                return
        except AttributeError:
            pass

        self.AQ_RANGES = []
        for i, (lower, (label, color)) in enumerate(
                zip(self.RANGES, self._LABELS_COLORS)):
            try:
                upper = self.RANGES[i + 1]
            except IndexError:
                # Set the upper bound with a sentinel value to indicate
                # no hard upper limit
                upper = -1

            self.AQ_RANGES.append(
                AirQualityRange(label, self.size, color, lower, upper)
                )

    def export_range_list(self) -> List[AirQualityRange]:
        """Export the air quality ranges as a list.

        Returns:
            List[AirQualityRange]: a list of air quality ranges,
                associated with the PM size

        Raises:
            ValueError: if self.AQ_RANGES is empty

        """
        if not self.AQ_RANGES:
            raise ValueError

        return self.AQ_RANGES


class AirQuality2_5(AirQuality):
    """Represents PM2.5. Attributes should match the base class."""

    RANGES = [0, 12, 35, 55, 150, 250]
    UPPER = 400

    def __init__(self) -> None:
        """Initialize the PM size."""
        self.size = 2.5
        self.populate_range_list()


class AirQuality10(AirQuality):
    """Represents PM10. Attributes should match the base class."""

    RANGES = [0, 55, 155, 255, 355, 425]
    UPPER = 500

    def __init__(self) -> None:
        """Initialize the PM size."""
        self.size = 10
        self.populate_range_list()


AQS = {
    2.5: AirQuality2_5(),
    10: AirQuality10(),
    }

COLORS = AirQuality().get_all_colors()
