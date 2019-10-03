#!/usr/bin/env python3
import os
import pika
import uuid

def on_response(ch, method, props, body):
    print(body)

host = str(os.getenv('RABBITMQ_HOST'))
port = int(os.getenv('RABBITMQ_PORT', 5672))
queue = os.getenv('RABBITMQ_QUEUE', 'auth-queue-rpc')
username = os.getenv('RABBITMQ_USER', 'auth')
password = os.getenv('RABBITMQ_PASS', 'authpass')

corr_id = str(uuid.uuid4())

credentials = pika.PlainCredentials(username, password)
params = pika.ConnectionParameters(host, port, '/', credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()

# Create callback queue
result = channel.queue_declare(queue='', exclusive=True)
callback_queue = result.method.queue

channel.basic_consume(
    queue=callback_queue,
    on_message_callback=on_response,
    auto_ack=True)

channel.basic_publish(exchange='',
    routing_key=queue,
    properties=pika.BasicProperties(
        reply_to=callback_queue,
        correlation_id=corr_id,
    ),
    body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
