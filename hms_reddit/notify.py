import logging
import threading


from hms_base.client import Client

from hms_reddit import settings


def get_logger():
    return logging.getLogger(__name__)


class Notifier:
    def __init__(self, addr, exchanger):

        # Create rabbit client
        self.topic = settings.RABBIT_TOPIC
        self.client = Client('hms_reddit', settings.RABBIT_EXCHANGER, [])

        self.client.connect(settings.RABBIT_HOST)

        def thread():
            self.client.consume()

        self.consume_thread = threading.Thread(target=thread, daemon=True)
        self.consume_thread.start()

    def notify(self, obj):

        if 'date' in obj:
            obj['date'] = obj['date'].isoformat()

        to_send = obj

        get_logger().info("Publishing message with routing key {}".format(
            self.topic))

        self.client.publish(self.topic, to_send)

    def disconnect(self):
        self.client.disconnect()
