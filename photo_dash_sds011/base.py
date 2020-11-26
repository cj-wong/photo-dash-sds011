from datetime import timedelta
from time import sleep

import pendulum
import requests

from photo_dash_sds011 import config


_REQUEST_ERRS = (
    requests.exceptions.ConnectionError,
    requests.exceptions.HTTPError,
    )


class BaseModule:
    """Base module for all photo-dash modules."""

    def __init__(self) -> None:
        """Nothing is initialized within the base module."""
        pass

    def setup_quiet_hours(self) -> None:
        """Set up quiet hours for the module.

        This function should be run every 24h to get the latest info.

        """
        now = pendulum.now()

        try:
            if now < self.last_check + timedelta(days=1):
                return
        except AttributeError:
            pass

        try:
            response = requests.get(f'{config.ENDPOINT}/quiet')
            response.raise_for_status()
            quiet_hours = response.json()
            config.LOGGER.info(f'Updating quiet hours: {quiet_hours}')
            self.quiet_setup = True
            self.quiet_start = quiet_hours['quiet_start']
            self.quiet_end = quiet_hours['quiet_end']
        except _REQUEST_ERRS:
            self.quiet_setup = False

        self.last_check = now

    def in_quiet_hours(self) -> bool:
        """Check whether the current time is within quiet hours.

        Returns:
            bool: True if within quiet hours

        Raises:
            AttributeError: if quiet hours weren't defined in config

        """
        now = pendulum.now()
        hour = now.hour
        if self.quiet_start > self.quiet_end:
            if hour >= self.quiet_start or hour < self.quiet_end:
                return True
        elif hour in range(self.quiet_start, self.quiet_end):
            return True

        return False

    def sleep_quiet_hours(self) -> None:
        """Sleep until quiet hours are over."""
        if not self.in_quiet_hours():
            return
        now = pendulum.now()
        days = 1 if now.hour > self.quiet_end else 0
        sleep_until = (
            pendulum.today()
            + timedelta(days=days, hours=self.quiet_end)
            )
        sleep((sleep_until - now).seconds)
