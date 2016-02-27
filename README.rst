reddithaum
==========

A small microservice that poll Reddit and publish new posts to a RabbitMQ
exchanger.

Using
-----

Create a Python 3 virtualenv and install dependencies::

    $ virtualenv -ppython3 venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt

Then start the bot when you are in the repository root folder::

    $ python run.py

Installing the systemd service
------------------------------

You need to copy the systemd service file onto your system and then enable and
start it using the following commands:

::

    # cp systemd/reddithaum.service /etc/systemd/system/multi.user.target.wants/
    # systemctl enable reddithaum
    # systemctl start reddithaum

Testing
-------

This project have both BDD tests (written in French) and unit tests. If you
want to run the tests to check you do not break things you first need to
install the dev. dependencies::

    (venv) $ pip install -r dev-requirements.txt

Then you can run the BDD tests using behave::

    (venv) $ behave

And the unit tests using nosetests::

    (venv) $ nosetests

License
-------

This project is brought to you under MIT license. For further information,
please read the provided LICENSE file.
