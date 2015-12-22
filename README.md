# reddithaum, un bot IRC pour Reddit

Un petit bot IRC qui poste les derniers liens postés sur le Reddit sur le canal
IRC du HAUM.

## Utilisation

Création d’un environnement virtuel Python 2 :

    $ virtualenv -ppython2 venv

Activation de l’environnement virtuel :

    $ source venv/bin/activate

Installation des dépendances :

    (venv) $ pip install -r requirements.txt

Lancement :

    $ python reddithaum/main.py

## Ressources

 - [twisted irc bot sample(ssl)](https://gist.github.com/shnmorimoto/1717671)
 - [Classe
   IRCClient (Twisted)](https://twistedmatrix.com/documents/15.4.0/api/twisted.words.protocols.irc.IRCClient.html)
