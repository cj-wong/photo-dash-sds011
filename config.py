import json
import logging
import logging.handlers


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


try:
    with open('config.json', 'r') as f:
        CONFIG = json.load(f)
    DEVICE = CONFIG['device']
    SLEEP = CONFIG['seconds_per_cycle']
except (FileNotFoundError, KeyError, TypeError, ValueError) as e:
    LOGGER.error('config.json doesn\'t exist or is malformed.')
    LOGGER.error(f'More information: {e}')
    raise e
