import unittest
from unittest.mock import Mock

from praw.errors import HTTPException

from hms_reddit.retrieve import Retriever


class RetrieveTestCase(unittest.TestCase):

    def test_reddit_404(self):
        notifier = Mock()
        notifier.notify = Mock()

        r = Retriever(notifier)

        # Simulate HTTP error of reddit
        r._retrieve_submissions = Mock(
            side_effect=HTTPException('error http'),
            return_value=['truc'])

        # Try to check submissions with HTTP error incoming.
        #
        # We want the exception to be catched in this method and not raised
        # outside of it.

        # Test that method returns nothing, aka. no exception thrown
        self.assertEqual(r.check_submissions(), None)

        # Test that the notifier was not called when exception occured
        notifier.notify.assert_not_called()