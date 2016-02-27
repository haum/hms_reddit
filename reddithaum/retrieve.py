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

from reddithaum import settings


def get_logger():
    return logging.getLogger(__name__)


def already_posted(sub):
    with open('posted') as f:
        posted = f.read().splitlines()
        return sub.id in posted


def mark_posted(sub):
    with open('posted', 'a') as f:
        f.write(sub['id'] + '\n')


def init_file():
    with open('posted', 'w') as f:
        f.flush()


class Retriever:
    def __init__(self, notifier):
        self.last_retrieve = None
        self.notifier = notifier

    def _retrieve_submissions(self):
        """Retrieve data from Reddit API."""
        r = praw.Reddit(user_agent=settings.USER_AGENT)
        submissions = r.get_subreddit('haum').get_hot(limit=5)

        for sub in filter(lambda x: not already_posted(x), submissions):
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

        if self.last_retrieve is not None and \
           self.last_retrieve > datetime.now() - timedelta(seconds=60):
            raise RuntimeError('Check submission is too fast')

        subs = self._retrieve_submissions()

        for sub in subs:
            self.notifier.notify(sub)
            mark_posted(sub)

        self.last_retrieve = datetime.now()


if __name__ == "__main__":
    init_file()
