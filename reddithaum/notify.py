import logging


from reddithaum import settings
from reddithaum.rabbit import RabbitClient


def get_logger():
    return logging.getLogger(__name__)


class Notifier:
    def __init__(self, addr, exchanger):

        # Create rabbit client
        self.routing_key = settings.RABBIT_ROUTING_KEY
        self.client = RabbitClient(exchange=exchanger, routing_keys=['ping'])

        self.client.connect(settings.RABBIT_HOST)

    def notify(self, obj):

        if 'date' in obj:
            obj['date'] = obj['date'].isoformat()

        to_send = obj

        get_logger().info("Publishing message with routing key {}".format(
            self.routing_key))

        self.client.publish(self.routing_key, to_send)
