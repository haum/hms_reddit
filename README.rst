reddithaum
==========

A small microservice that poll Reddit and publish new posts to a RabbitMQ
exchanger.

Using
-----

Create a Python 3 virtualenv:

::

    $ virtualenv -ppython3 venv

Activate virtualenv:

::

    $ source venv/bin/activate

Install dependencies:

::

    (venv) $ pip install -r requirements.txt

Finally start the bot when you are in the repository root folder:

::

    $ python run.py

Installing the systemd service
------------------------------

You need to copy the systemd service file onto your system and then enable and
start it using the following commands:

::

    # cp systemd/reddithaum.service /etc/systemd/system/multi.user.target.wants/
    # systemctl enable reddithaum
    # systemctl start reddithaum

License
-------

This project is brought to you under MIT license. For further information,
please read the provided LICENSE file.
