import pika
import json


class Notifier:
    def __init__(self, addr, exchanger):
        self.exchanger = exchanger

        params = pika.ConnectionParameters(addr)
        self.conn = pika.BlockingConnection(params)
        self.channel = self.conn.channel()

        self.channel.exchange_declare(exchange=exchanger, type='fanout')

    def notify(self, obj):

        if 'date' in obj:
            obj['date'] = obj['date'].isoformat()

        js = json.dumps(obj)

        self.channel.basic_publish(
            exchange=self.exchanger,
            routing_key='',
            body=js)
