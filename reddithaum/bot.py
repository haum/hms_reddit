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

import sys

import irc.bot

import settings
from logger import MessageLogger
from reddit import mark_posted, get_submissions


class MyBot(irc.bot.SingleServerIRCBot):

    """A Reddit checker bot."""

    def __init__(self, channel, nickname, server, port=6667):
        super().__init__([(server, port)], nickname, nickname)
        self.channel = channel
        self.logger = MessageLogger(sys.stdout)


    def on_welcome(self, serv, ev):
        self.logger.log("signed on")
        self.logger.log("joining {}".format(self.channel))
        serv.join(self.channel)


    def on_join(self, serv, ev):
        self.logger.log("joined {}".format(self.channel))
        self.connection.execute_every(settings.SLEEP, self._check_submissions, (serv,))
        self._check_submissions(serv)


    def on_kick(self, serv, ev):
        die('got kicked')
        #serv.join(self.channel)


    def on_nicknameinuse(self, serv, ev):
        newnick = serv.get_nickname() + '_'
        self.logger.log("nick in use, using {}".format(newnick))
        serv.nick(newnick)


    def _check_submissions(self, serv):
        self.logger.log("checking for new submissions ({})".format(settings.USER_AGENT))
        submissions = get_submissions()

        for x in submissions:
            m = "[{}] {} -> {}".format(x.id, x.title, x.url)
            self.logger.log("posting {}".format(x.id))
            serv.privmsg(self.channel, m)
            self.logger.log("marking {} as posted".format(x.id))
            mark_posted(x)

        self.logger.log("finished checking new submissions")
