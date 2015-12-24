# reddithaum

A small IRC bot that post the latest Reddit submissions on an IRC channel.

## Using

Create a Python 2 virtualenv:

    $ virtualenv -ppython2 venv

Activate virtualenv:

    $ source venv/bin/activate

Install dependencies:

    (venv) $ pip install -r requirements.txt

Finally start the bot:

    $ python reddithaum/main.py

## License

This project is brought to you under MIT license. For further information,
please read the provided LICENSE file.

## Ressources

 - [twisted irc bot sample(ssl)](https://gist.github.com/shnmorimoto/1717671)
 - [Classe
   IRCClient (Twisted)](https://twistedmatrix.com/documents/15.4.0/api/twisted.words.protocols.irc.IRCClient.html)
