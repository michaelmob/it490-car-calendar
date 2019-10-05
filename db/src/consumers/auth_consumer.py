import os
import json
from amqp.consumer import Consumer
from pika import BasicProperties



class AuthConsumer:
    """
    Authentication consumer.
    Accepts JSON messages.
    """

    def __init__(self, host, port, vhost, username, password):
        """
        Initialize authentication consumer.
        """
        self.consumer = Consumer(host, port, vhost, username, password)
        self.consumer.init_message = '[*] Waiting for auth messages. To exit press CTRL+C'


    def consume(self, queue, callback):
        """
        Consume auth queue.
        """
        self.extra_callback = callback
        self.consumer.consume(queue, self.callback)


    def callback(self, ch, method, props, body):
        """
        Authenticate user callback.
        """
        # If there is a reply_to property then it's an RPC
        # We don't care about non-RPC calls
        if props.reply_to:
            return

        # Get response from callback defined by consume
        response = None
        if callable(self.extra_callback):
            response = self.extra_callback(ch, method, props, body)

        # Response cannot be nothing
        if not response:
            return

        # Publish response to exchange
        ch.basic_publish(exchange='',
             routing_key=props.reply_to,
             properties=BasicProperties(correlation_id=props.correlation_id),
             body=str(json.dumps(response)))
