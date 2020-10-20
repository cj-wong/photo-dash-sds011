import unittest

from photo_dash_sds011 import config


class TestConfig(unittest.TestCase):
    """Test the config module."""

    def test_get_range(self) -> bool:
        """Test whether get_range() behaves as expected.

        Tests the following:
        - that pm must be 2.5 or 10

        """
        self.assertRaises(KeyError, config.get_range, 3, 0)


if __name__ == '__main__':
    unittest.main()
