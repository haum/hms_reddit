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
import logging
import time

from requests.exceptions import ReadTimeout
import coloredlogs

from hms_reddit import settings
from hms_reddit.retrieve import Retriever
from hms_reddit.notify import Notifier

from pika.exceptions import ConnectionClosed


def get_logger():
    return logging.getLogger(__name__)


def poll_loop(no, ret):
    while True:
        try:
            get_logger().info('Checking new submissions...')
            ret.check_submissions()
        except ReadTimeout:
            get_logger().error('Read timeout, restarting bot.')
        except ConnectionClosed:
            get_logger().error(
                'Disconnected from RabbitMQ, restarting bot.')
            no = Notifier(settings.RABBIT_HOST, settings.RABBIT_EXCHANGER)
            ret = Retriever(no)
        except RuntimeError as e:
            get_logger().error(e)
        finally:
            time.sleep(settings.POLL_REDDIT_EVERY.seconds)


def main():
    # Logging
    coloredlogs.install(level='INFO')

    # Create objects
    no = Notifier(settings.RABBIT_HOST, settings.RABBIT_EXCHANGER)
    ret = Retriever(no)

    # Poll
    try:
        poll_loop(no, ret)
    except KeyboardInterrupt:
        get_logger().critical("Got a KeyboardInterrupt")
        get_logger().info("Disconnecting from RabbitMQ")
        no.disconnect()

        get_logger().info("Goodbye")
        sys.exit(0)
