import logging
import json

import pika

from reddithaum import settings


def get_logger():
    return logging.getLogger(__name__)


class Notifier:
    def __init__(self, addr, exchanger):
        self.exchanger = exchanger
        self.routing_key = settings.RABBIT_ROUTING_KEY

        params = pika.ConnectionParameters(addr)

        get_logger().info("Connecting to RabbitMQ server...")
        self.conn = pika.BlockingConnection(params)

        get_logger().info("Creating channel...")
        self.channel = self.conn.channel()

        get_logger().info("Declaring exchanger...")
        self.channel.exchange_declare(
            exchange=exchanger, exchange_type='direct')

    def notify(self, obj):

        if 'date' in obj:
            obj['date'] = obj['date'].isoformat()

        to_send = obj

        get_logger().info("Publishing message with routing key {}".format(
            self.routing_key))

        self.channel.basic_publish(
            exchange=self.exchanger,
            routing_key=self.routing_key,
            body=json.dumps(to_send))
