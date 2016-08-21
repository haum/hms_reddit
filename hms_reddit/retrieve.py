# Copyright (c) 2015 Romain Porte (MicroJoe)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import logging
from datetime import datetime, timedelta

import praw

from hms_reddit import settings
from hms_reddit.security import VeganWatchdog


def get_logger():
    return logging.getLogger(__name__)


class PostDatabase:

    """Class containing static calls for post database handling"""

    @staticmethod
    def already_posted(sub):
        """Check if a post was already posted."""
        with open('posted') as f:
            posted = f.read().splitlines()
            return sub.id in posted

    @staticmethod
    def mark_posted(sub):
        """Mark a post as posted."""
        with open('posted', 'a') as f:
            f.write(sub['id'] + '\n')

    @staticmethod
    def init_file():
        """Creates the empty database file."""
        with open('posted', 'w') as f:
            f.flush()


class Retriever:

    """Object used to retrieve Reddit news using the praw library."""

    def __init__(self, notifier):
        """Default constructor."""
        self.notifier = notifier
        self.watchdog = VeganWatchdog(settings.POLL_REDDIT_EVERY)

    def _retrieve_submissions(self):
        """Retrieve new posts from Reddit API."""

        # Retrieve posts
        r = praw.Reddit(user_agent=settings.USER_AGENT)
        submissions = r.get_subreddit('haum').get_hot(limit=5)

        # We only yield the submissions that we did not already posted
        filtered_subs = filter(
            lambda x: not PostDatabase.already_posted(x), submissions)

        for sub in filtered_subs:
            yield {
                'id': sub.id,
                'author': sub.author.name,
                'title': sub.title,
                'url': sub.url,
                'date': datetime.now()
            }

    def check_submissions(self):
        """Check data from API and send new posts to notifier.

        This method is protected against mass call so the program will not
        get banned from Reddit for spamming its API.

        """

        # Feed the watchdog that will raise an exception if called too often in
        # order to protect the bot from being banned
        self.watchdog.feed()

        # Retrieve new posts, handling possible HTTP error
        subs = []
        try:
            subs = self._retrieve_submissions()
        except praw.errors.HTTPException as e:
            get_logger().error("HTTPException from praw : {}".format(e))

        # Notify each new post and mark it as already posted
        for sub in subs:
            self.notifier.notify(sub)
            PostDatabase.mark_posted(sub)


# If this module is started standalone, we want to create the empty database
# file
if __name__ == "__main__":
    PostDatabase.init_file()
