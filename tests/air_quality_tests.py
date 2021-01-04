import unittest

from photo_dash_sds011 import air_quality


class TestConfig(unittest.TestCase):
    """Test the air_quality module.

    Tests the following:

        1. That the lower bound for both pm2.5 and pm10 works
        2. That a very high number should be labeled 'Hazardous'

    """

    def test_get_range_lower_bound(self) -> None:
        """Test get_range() lower bounds. Test #1 in class docstring."""
        self.assertEqual(
            air_quality.AQS[2.5].get_range(0),
            air_quality.asdict(air_quality.AQS[2.5].AQ_RANGES[0])
            )
        self.assertEqual(
            air_quality.AQS[10].get_range(355),
            air_quality.asdict(air_quality.AQS[10].AQ_RANGES[4])
            )

    def test_get_range_high_reading(self) -> None:
        """Test get_range() for a very high reading. Test #2."""
        for pm in (2.5, 10):
            aq = air_quality.AQS[pm]
            self.assertEqual(
                aq.get_range(aq.RANGES[-1] + 1)['label'],
                'Hazardous'
                )


if __name__ == '__main__':
    unittest.main()
