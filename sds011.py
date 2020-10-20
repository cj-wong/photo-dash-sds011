import time

import serial

import config

# Adapted from:
#   https://www.raspberrypi.org/blog/monitor-air-quality-with-a-raspberry-pi/


class SDS011:
    """Represents the SDS011 air quality sensor.

    Attributes:
        data (List[])
        sensor (serial.serialposix.Serial): the SDS011 over serial

    """

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
            pm2_5 = self.read_data_from_bytes(2, 4)
            pm10 = self.read_data_from_bytes(4, 6)

    def read_data_from_bytes(self, start: int, stop: int) -> int:
        """Read the particulate data from bytes from the sensor.

        Args:
            start (int): starting index
            stop (int): stopping index; reading stops before reaching this
                index

        Returns:
            int: particulate reading of unit μg / m^3
                (micrograms per cubic meter)

        """
        return int.from_bytes(
            b''.join(self.data[start:stop]), byteorder='little'
        ) / 10


if __name__ == '__main__':
    s = SDS011()
