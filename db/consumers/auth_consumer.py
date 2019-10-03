#!/usr/bin/env python3
import os
import json
from consumer import Consumer, Producer
from pika import BasicProperties



class AuthConsumer:
    """
    Authentication consumer.
    Excepts JSON messages.
    """

    def __init__(self, host, port, vhost, auth_username, auth_password,
                 log_username, log_password):
        """
        Initialize authentication consumer.
        """
        self.consumer = Consumer(host, port, vhost, auth_username, auth_password)
        self.consumer.init_message = '[*] Waiting for auth messages. To exit press CTRL+C'
        self.producer = Producer(host, port, vhost, log_username, log_password)


    def consume(self, auth_queue, log_queue):
        """
        Consume auth queue.
        """
        self.auth_queue = auth_queue
        self.log_queue = log_queue
        self.consumer.consume(auth_queue, self.callback)


    def callback(self, ch, method, props, body):
        """
        Authenticate user callback.
        """
        if props.reply_to:
            return

        self.authenticate(json.loads(body))

        ch.basic_publish(exchange='',
             routing_key=props.reply_to,
             properties=BasicProperties(correlation_id=props.correlation_id),
             body=str('test'))


    def log_login_attempt(self, username, success):
        """
        Log the attempted login.
        """
        self.producer.produce('log msg', self.log_queue)


    def authenticate(self, data):
        """
        Attempt to authenticate from the database.
        """
        pass


if __name__ == '__main__':
    # Config
    host = str(os.getenv('RABBITMQ_HOST'))
    port = int(os.getenv('RABBITMQ_PORT', 5672))
    vhost = os.getenv('RABBITMQ_VHOST', '/')

    # Auth credentials
    username = os.getenv('RABBITMQ_USER', 'auth')
    password = os.getenv('RABBITMQ_PASS', 'authpass')
    auth_queue = os.getenv('RABBITMQ_QUEUE', 'auth-queue-rpc')

    # Logging credentials
    log_username = os.getenv('RABBITMQ_LOG_USER', 'log')
    log_password = os.getenv('RABBITMQ_LOG_PASS', 'logpass')
    log_queue = os.getenv('RABBITMQ_LOG_QUEUE', 'log-queue')

    # Start consuming
    auth_consumer = AuthConsumer(host, port, vhost, username, password, log_username, log_password)
    auth_consumer.consume(auth_queue, log_queue)
