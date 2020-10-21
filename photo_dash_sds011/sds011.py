import time

import serial

from photo_dash_sds011 import config

# Adapted from:
#   https://www.raspberrypi.org/blog/monitor-air-quality-with-a-raspberry-pi/


class SDS011:
    """Represents the SDS011 air quality sensor.

    Attributes:
        data (List[])
        sensor (serial.serialposix.Serial): the SDS011 over serial

    """

    _SLICES = {2.5: 2, 10: 4}

    def __init__(self) -> None:
        """Initialize the serial device given the path config.DEVICE."""
        self.sensor = serial.Serial(config.DEVICE)

    def loop(self) -> None:
        """Loop through reading the sensor every n seconds.

        n is config.SLEEP.

        """
        while True:
            # Sleep before running code to ensure that the sensor is
            # initialized on first run, as per the specifications.
            time.sleep(config.SLEEP)
            self.data = []
            for _ in range(10):
                datum = self.sensor.read()
                self.data.append(datum)

            for pm, start in self._SLICES.items():
                reading = self.read_data_from_bytes(start)
                aq_dict = config.get_range(pm, reading)

    def read_data_from_bytes(self, start: int) -> int:
        """Read the particulate data from bytes from the sensor.

        Args:
            start (int): starting index; 'stop' is start + 2

        Returns:
            int: particulate reading of unit μg / m^3
                (micrograms per cubic meter)

        """
        stop = start + 2
        return int.from_bytes(
            b''.join(self.data[start:stop]), byteorder='little'
            ) / 10


if __name__ == '__main__':
    s = SDS011()
