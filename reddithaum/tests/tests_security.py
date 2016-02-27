import unittest
from datetime import datetime, timedelta

from reddithaum.security import VeganWatchdog


class TestVeganWatchdog(unittest.TestCase):

    """Test the implementation of the reverse watchdog."""

    def setUp(self):
        self.dog = VeganWatchdog(timedelta(seconds=60))

    def test_first_feed(self):
        self.dog.feed()

    def test_feed_too_fast(self):
        short_ago = datetime.now() - self.dog.mintime + timedelta(seconds=1)

        self.dog.last_call = short_ago

        with self.assertRaises(RuntimeError):
            self.dog.feed()

    def test_feed_slowly(self):
        long_ago = datetime.now() - self.dog.mintime - timedelta(seconds=1)

        self.dog.last_call = long_ago
        self.dog.feed()
