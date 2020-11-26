import json
import logging
import logging.handlers


_LOGGER_NAME = 'photo-dash-sds011'

LOGGER = logging.getLogger(_LOGGER_NAME)
LOGGER.setLevel(logging.DEBUG)

FH = logging.handlers.RotatingFileHandler(
    f'{_LOGGER_NAME}.log',
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
    ENDPOINT = CONFIG['endpoint']
    # Module-specific config continues below
    DEVICE = CONFIG['device']
    SLEEP = CONFIG['seconds_per_cycle']
    if not isinstance(SLEEP, int):
        # Coerce a type conversion. If this doesn't work, ValueError will be
        # correctly raised and terminate the program.
        SLEEP = int(SLEEP)
    # Module-specific config ends here
except CONFIG_LOAD_ERRORS as e:
    LOGGER.error('config.json doesn\'t exist or is malformed.')
    LOGGER.error(f'More information: {e}')
    raise e

# Remaining module-specific code continues below

try:
    DC_QH = CONFIG['disconnect_in_quiet_hours']
except KeyError:
    DC_QH = False
