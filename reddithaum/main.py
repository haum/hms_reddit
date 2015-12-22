from twisted.internet import reactor

from bot import LogBotFactory


if __name__ == "__main__":
    reactor.connectTCP("irc.freenode.net", 6667, LogBotFactory())
    reactor.run()
