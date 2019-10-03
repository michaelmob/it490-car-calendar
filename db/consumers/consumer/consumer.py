#!/usr/bin/env python3
import pika



class Consumer:
    """
    Queue consumer.
    """

    def __init__(self, host, port, vhost, username, password):
        """
        Initialize LogConsumer.
        """
        credentials = pika.PlainCredentials(username, password)
        params = pika.ConnectionParameters(host, port, vhost, credentials)
        connection = pika.BlockingConnection(params)
        self.channel = connection.channel()
        self.init_message = None


    def consume(self, queue, callback):
        """
        Consuming listener.
        """
        self.extra_callback = callback
        self.channel.queue_declare(queue=queue)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue, on_message_callback=self.consume_callback)
        print(self.init_message or '[*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()


    def consume_callback(self, ch, method, props, body):
        """
        Called on consume.
        """
        if callable(self.extra_callback):
            self.extra_callback(ch, method, props, body)

        print("[x] Received %r" % body)
        ch.basic_ack(delivery_tag=method.delivery_tag)
