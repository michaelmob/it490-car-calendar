import time
import pika
import uuid



class Producer:
    """
    Queue producer.
    """

    def __init__(self, host, port, vhost, username, password, is_rpc=False, rpc_attempts=25):
        """
        Initialize Producer instance.
        """
        self.is_rpc = is_rpc
        self.rpc_attempts = rpc_attempts

        # RabbitMQ Auth
        credentials = pika.PlainCredentials(username, password)
        params = pika.ConnectionParameters(
            host, port, vhost, credentials,
            socket_timeout=3, stack_timeout=3
        )
        self.connection = pika.BlockingConnection(params)
        self.channel = self.connection.channel()

        if self.is_rpc:
            # Create a callback queue
            result = self.channel.queue_declare(queue='', exclusive=True)
            self.callback_queue = result.method.queue

            # Receive responses from the callback queue
            self.channel.basic_consume(
                queue=self.callback_queue,
                on_message_callback=self.response_callback,
                auto_ack=True
            )


    def produce(self, queue, value):
        """
        Send a value and wait for a response.
        """
        self.response = None

        # Add tracking info to the value thats about to be published if RPC
        props = None
        if self.is_rpc:
            self.corr_id = str(uuid.uuid4())
            props = pika.BasicProperties(
                reply_to=self.callback_queue, correlation_id=self.corr_id
            )

        # Publish value to exchange
        self.channel.basic_publish(
            exchange='',
            routing_key=queue,
            properties=props,
            body=str(value)
        )

        # Wait for response if RPC.
        if self.is_rpc:
            attempts = 0
            while self.response is None:
                # Try to retrieve data
                self.connection.process_data_events()

                # Increment attempts or break if attempts have been exceeded
                if self.response is None:
                    attempts += 1
                    if attempts >= self.rpc_attempts:
                        break

                    time.sleep(0.1)  # This isn't good. But it saves my CPU.

        return self.response


    def response_callback(self, ch, method, props, body):
        """
        Called on RPC response.
        """
        if self.corr_id == props.correlation_id:
            self.response = body
