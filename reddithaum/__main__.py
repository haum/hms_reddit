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
import time

from requests.exceptions import ReadTimeout

import settings
from retrieve import Retriever
from notify import Notifier


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)-15s [%(levelname)s] (%(name)s) %(message)s',
        level=logging.INFO)

    no = Notifier(settings.RABBIT_ADDR, settings.RABBIT_EXCHANGER)
    ret = Retriever(no)

    while True:
        try:
            logging.info('Checking new submissions...')
            ret.check_submissions()
        except ReadTimeout:
            logging.error('Read timeout, restarting bot.')
        except RuntimeError as e:
            logging.error(e)
        finally:
            time.sleep(3)
