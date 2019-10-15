import json
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
        params = pika.ConnectionParameters(
            host, port, vhost, credentials, socket_timeout=3, retry_delay=3
        )
        connection = pika.BlockingConnection(params)
        self.channel = connection.channel()


    def consume(self, queue, callback):
        """
        Consuming listener.
        """
        self.extra_callback = callback
        self.channel.queue_declare(queue=queue)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue, on_message_callback=self.callback)
        self.channel.start_consuming()


    def callback(self, ch, method, props, body):
        """
        Called on consume.
        """
        print("-> Received %r" % body)

        # If we have a property in props called 'reply_to' then its an RPC
        if props and props.reply_to:
            # Get response from callback defined by consume
            response = None
            if callable(self.extra_callback):
                response = self.extra_callback(ch, method, props, body)

            # Response cannot be nothing
            if not response:
                return

            print("<- Sent %r" % response)

            # Publish response to exchange
            ch.basic_publish(
                exchange='',
                routing_key=props.reply_to,
                properties=pika.BasicProperties(correlation_id=props.correlation_id),
                body=str(json.dumps(response))
            )

        # No 'reply_to' property, so its just a hit-n-run
        elif callable(self.extra_callback):
            self.extra_callback(ch, method, props, body)

        ch.basic_ack(delivery_tag=method.delivery_tag)
