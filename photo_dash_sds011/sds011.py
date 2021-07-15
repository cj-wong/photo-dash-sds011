from time import sleep

import requests
import serial

from photo_dash_sds011 import air_quality
from photo_dash_sds011 import base
from photo_dash_sds011 import config


# Adapted from:
#   https://www.raspberrypi.org/blog/monitor-air-quality-with-a-raspberry-pi/


class SDS011(base.BaseModule):
    """Represents the SDS011 air quality sensor.

    Attributes:
        data (List[bytes]): a list of bytes as described in specs;
            data will be cleared every loop start; for more information,
            see here: http://ecksteinimg.de/Datasheet
                /SDS011%20laser%20PM2.5%20sensor%20specification-V1.3.pdf
        init_time (pendulum.datetime): when the module was started
        quiet_start (int): hour to stop reading and sending data
        quiet_end (int): hour to resume reading and sending data
        sensor (serial.serialposix.Serial): the SDS011 over serial

    """

    _SLICES = {2.5: 2, 10: 4}

    def __init__(self) -> None:
        """Initialize the serial device given the path config.DEVICE."""
        self.sensor = serial.Serial(config.DEVICE)
        super().__init__()

    def loop(self) -> None:
        """Loop through reading the sensor every n seconds.

        n is config.SLEEP.

        """
        while True:
            # Sleep before running code to ensure that the sensor is
            # initialized on first run, as per the specifications.
            sleep(config.SLEEP)

            self.setup_quiet_hours()

            if self.quiet_setup:
                if self.in_quiet_hours():
                    if config.DC_QH:
                        self.sensor.close()
                    self.sleep_quiet_hours()
                    continue

            # In the case that quiet hours were established during first run
            # and removed from the endpoint afterwards, the sensor may not
            # be in the open state. Because serial.Serial.open() may raise
            # an exception if the sensor is already open, just check prior.
            if not self.sensor.isOpen():
                self.sensor.open()

            config.LOGGER.info('Woke up after sleeping. Running loop()')
            self.data = []
            for _ in range(10):
                datum = self.sensor.read()
                self.data.append(datum)

            for pm, start in self._SLICES.items():
                # Might be necessary to give the endpoint some time
                # between responses
                sleep(10)
                reading = self.read_data_from_bytes(start)
                aq_dict = air_quality.AQS[pm].get_range(reading)

                sections = [
                    {
                        'type': 'text',
                        'color': aq_dict['color'],
                        'value': f'Quality: {aq_dict["label"]}'
                        },
                    {
                        'type': 'gauge',
                        'color': [aq_dict['color']],
                        'range': [aq_dict['lower'], aq_dict['upper']],
                        'value': reading,
                        },
                    {
                        'type': 'gauge',
                        'color': air_quality.COLORS,
                        'range': air_quality.AQS[pm].get_all_ranges(),
                        'value': reading,
                        }
                    ]

                data = {
                    'module': f'photo-dash-sds011-pm{pm}',
                    'title': f'Air Quality - PM{pm}',
                    'sections': sections,
                    }

                try:
                    r = requests.put(config.ENDPOINT, json=data)
                except Exception as e: # Catching broad Exceptions for now
                    config.LOGGER.error(e)
                config.LOGGER.info(r.status_code)

    def read_data_from_bytes(self, start: int) -> float:
        """Read the particulate data from bytes from the sensor.

        Args:
            start (int): starting index; 'stop' is start + 2

        Returns:
            float: particulate reading of unit μg / m^3
                (micrograms per cubic meter)

        """
        stop = start + 2
        return int.from_bytes(
            b''.join(self.data[start:stop]), byteorder='little'
            ) / 10
