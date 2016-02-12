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

import irc.bot
import praw

import settings
from security import VeganWatchdog
from reddit import mark_posted, get_submissions


def get_logger():
    return logging.getLogger(__name__)


class MyBot(irc.bot.SingleServerIRCBot):

    """A Reddit checker bot."""

    def __init__(self, channel, nickname, server, port=6667):
        super().__init__([(server, port)], nickname, nickname)
        self.channel = channel
        self.rwatchdog = VeganWatchdog(settings.REVERSE_WATCHDOG_TIMEOUT)

    def on_welcome(self, serv, ev):
        get_logger().info("Signed on")
        get_logger().info("Joining {}".format(self.channel))
        serv.join(self.channel)

    def on_join(self, serv, ev):
        get_logger().info("Joined {}".format(self.channel))

        self.connection.execute_every(
            settings.POLL_REDDIT_EVERY, self._check_submissions, (serv,))
        self._check_submissions(serv)

    def on_kick(self, serv, ev):
        get_logger().warning("Kicked")
        self.die('got kicked')
        # serv.join(self.channel)

    def on_nicknameinuse(self, serv, ev):
        newnick = serv.get_nickname() + '_'
        get_logger().warning("Nick already in use, using {}".format(newnick))
        serv.nick(newnick)

    def _check_submissions(self, serv):

        try:
            self.rwatchdog.feed()
        except RuntimeError:
            get_logger().warning(
                "Reverse watchdog interrupted request to Reddit API")
            return

        get_logger().info(
            "Checking for new submissions ({})".format(settings.USER_AGENT))
        submissions = get_submissions()

        try:
            for x in submissions:
                m = "[{}] {} -> {}".format(x.author.name, x.title, x.url)

                get_logger().info("Posting {}".format(x.id))
                serv.privmsg(self.channel, m)

                get_logger().info("Marking {} as posted".format(x.id))
                mark_posted(x)

        except praw.errors.HTTPException:
            get_logger().warning(
                "Could not retrieve data from Reddit (HTTP error)")

        get_logger().info("Finished checking new submissions")
