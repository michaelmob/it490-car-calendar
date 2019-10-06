#!/usr/bin/env python3
import os
from dotenv import load_dotenv  # Load environment variables from env file first
load_dotenv(os.getenv('AUTH_ENV', '../.env_auth'))

import pika
import uuid
import json


class AuthRpcClient(object):

    def __init__(self):
        host = str(os.getenv('RABBITMQ_HOST'))
        port = int(os.getenv('RABBITMQ_PORT', 5672))
        queue = os.getenv('RABBITMQ_QUEUE')
        username = os.getenv('RABBITMQ_USER')
        password = os.getenv('RABBITMQ_PASS')
        credentials = pika.PlainCredentials(username, password)
        params = pika.ConnectionParameters(host, port, '/', credentials)
        self.connection = pika.BlockingConnection(params)

        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

    def call(self, data):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=os.getenv('RABBITMQ_AUTH_QUEUE', 'auth-queue-rpc'),
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(data))
        while self.response is None:
            self.connection.process_data_events()
        return self.response


auth_rpc = AuthRpcClient()

print("<- Requesting")

# Register
response = auth_rpc.call({
    'action': 'register',
    'email': 'test@test.com',
    'username': 'mike',
    'password': 'password'
})

print('-> Received')
print(json.loads(response))

# Login
response = auth_rpc.call({
    'action': 'login',
    'username': 'mike_REMOVE_THIS_TO_LOGIN',
    'password': 'password'
})

print('-> Received')
print(json.loads(response))
