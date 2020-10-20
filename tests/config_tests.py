import unittest

from photo_dash_sds011 import config


class TestConfig(unittest.TestCase):
    """Test the config module."""

    def test_get_range(self) -> bool:
        """Test whether get_range() behaves as expected.

        Tests the following:
        - that the lower bound for both pm2.5 and pm10 works
        - that a very high number should be labeled 'Hazardous'
        - that pm must be 2.5 or 10 AND an error should be logged

        """
        self.assertEqual(
            config.get_range(2.5, 0),
            config.asdict(config.RANGES[2.5][0])
            )
        self.assertEqual(
            config.get_range(10, 355),
            config.asdict(config.RANGES[10][4])
            )
        with self.assertLogs(logger=config.LOGGER, level=config.logging.ERROR):
            self.assertRaises(KeyError, config.get_range, 3, 0)


if __name__ == '__main__':
    unittest.main()
