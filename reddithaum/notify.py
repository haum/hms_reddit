import pika
import json


class Notifier:
    def __init__(self, addr, exchanger):
        self.exchanger = exchanger
        self.routing_key = 'reddit'

        params = pika.ConnectionParameters(addr)
        self.conn = pika.BlockingConnection(params)
        self.channel = self.conn.channel()

        self.channel.exchange_declare(exchange=exchanger, type='direct')

    def notify(self, obj):

        if 'date' in obj:
            obj['date'] = obj['date'].isoformat()

        to_send = obj

        self.channel.basic_publish(
            exchange=self.exchanger,
            routing_key=self.routing_key,
            body=json.dumps(to_send))
