import json
import logging
import logging.handlers
from dataclasses import asdict, dataclass
from typing import Dict, Union


LOGGER = logging.getLogger('photo-dash-sds011')
LOGGER.setLevel(logging.DEBUG)

FH = logging.handlers.RotatingFileHandler(
    'photo-dash-sds011.log',
    maxBytes=40960,
    backupCount=5,
    )
FH.setLevel(logging.DEBUG)

CH = logging.StreamHandler()
CH.setLevel(logging.WARNING)

FORMATTER = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
FH.setFormatter(FORMATTER)
CH.setFormatter(FORMATTER)

LOGGER.addHandler(FH)
LOGGER.addHandler(CH)

CONFIG_LOAD_ERRORS = (
    FileNotFoundError,
    KeyError,
    TypeError,
    ValueError,
    json.decoder.JSONDecodeError,
    )


try:
    with open('config.json', 'r') as f:
        CONFIG = json.load(f)
    DEVICE = CONFIG['device']
    SLEEP = CONFIG['seconds_per_cycle']
    if not isinstance(SLEEP, int):
        # Coerce a type conversion. If this doesn't work, ValueError will be
        # correctly raised and terminate the program.
        SLEEP = int(SLEEP)
except CONFIG_LOAD_ERRORS as e:
    LOGGER.error('config.json doesn\'t exist or is malformed.')
    LOGGER.error(f'More information: {e}')
    raise e


@dataclass
class AirQuality:
    """Represents air quality ranges.

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

    def is_range(self, reading: int) -> bool:
        """Check if reading fits within the range.

        Args:
            reading (int): an air quality reading

        """
        # Special case: no upper bound, only a lower bound
        if self.upper == 0 and self.upper < self.lower:
            return self.lower <= reading
        else:
            return self.lower <= reading and reading < self.upper


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

_AQ_PM_RANGES = {
    2.5: [0, 12, 35, 55, 150, 250],
    10: [0, 55, 155, 255, 355, 425]
    }

RANGES = {}

for pm, ranges in _AQ_PM_RANGES.items():
    RANGES[pm] = []
    for i, lower in enumerate(ranges):
        try:
            upper = ranges[i + 1]
        except IndexError:
            upper = 0

        label, color = _LABELS_COLORS[i]

        RANGES[pm].append(
            AirQuality(label, pm, color, lower, upper)
            )


def get_range(pm: float, reading: float) -> Dict[str, Union[str, float]]:
    """Get the appropriate AirQuality range given reading and pm.

    Args:
        pm (float): either 2.5 or 10 (PM2.5, PM10)
        reading (float): an air quality reading from the sensor

    Returns:
        Dict[str, Union[str, float]]: a dictionary containing the
            range's parameters

    Raises:
        KeyError: if pm wasn't 2.5 or 10

    """
    try:
        for aq in RANGES[pm]:
            if aq.is_range(reading):
                return asdict(aq)
    except KeyError as e:
        LOGGER.error(f'pm should be 2.5 or 10; supplied {pm}')
        raise e
