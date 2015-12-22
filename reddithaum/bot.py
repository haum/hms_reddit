import sys

from twisted.words.protocols import irc
from twisted.internet.protocol import ClientFactory
from twisted.internet import reactor

from logger import MessageLogger
from reddit import get_submissions

import settings
from reddit import mark_posted, get_submissions


class LogBot(irc.IRCClient):
    """A logging IRC bot."""

    nickname = settings.NICKNAME

    def connectionMade(self):
        """Called when bot has connected."""
        self.logger = self.factory.logger
        irc.IRCClient.connectionMade(self)
        self.logger.log("connected")

    def connectionLost(self, reason):
        """Called when bot has disconnected."""
        irc.IRCClient.connectionLost(self, reason)
        self.logger.log("disconnected")

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        self.logger.log("signed on")
        self.logger.log("joining {}".format(self.factory.channel))
        self.join(self.factory.channel)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        self.logger.log("joined {}".format(channel))
        self.check_submissions()

    def check_submissions(self):
        self.logger.log("checking for new submissions ({})".format(settings.USER_AGENT))
        submissions = get_submissions()

        for x in submissions:
            m = u"[{}] {} -> {}".format(x.id, x.title, x.url).encode('utf-8')
            self.msg(settings.CHAN, m)
            self.logger.log("posting and marking as posted {}".format(x.id))
            mark_posted(x)

        self.logger.log("finished, waiting for {}s".format(settings.SLEEP))
        reactor.callLater(60, self.check_submissions)



class LogBotFactory(ClientFactory):
    """A factory for LogBots.
    A new protocol instance will be created each time we connect to the server.
    """
    protocol = LogBot

    def __init__(self):
        self.channel = settings.CHAN
        self.logger = MessageLogger(sys.stdout)

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        reactor.stop()
