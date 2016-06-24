==========
hms_reddit
==========

A small microservice that poll Reddit and publish new posts to a RabbitMQ
exchanger.

Using
=====

Create a Python 3 virtualenv and install dependencies::

    $ virtualenv -ppython3 venv
    $ source venv/bin/activate
    (venv) $ pip install .

Then start the bot inside the virtualenv::

    (venv) $ hms_reddit

Installing the systemd service
==============================

You need to copy the systemd service file onto your system and then enable and
start it using the following commands:

::

    # make install
    # systemctl enable reddithaum
    # systemctl start reddithaum

License
-------

This project is brought to you under MIT license. For further information,
please read the provided ``LICENSE.txt`` file.
