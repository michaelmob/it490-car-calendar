#!/usr/bin/env python3
import os
import pika

host = str(os.getenv('RABBITMQ_HOST'))
port = int(os.getenv('RABBITMQ_PORT', 5672))
queue = os.getenv('RABBITMQ_QUEUE', 'log-queue')
username = os.getenv('RABBITMQ_USER', 'log')
password = os.getenv('RABBITMQ_PASS', 'logpass')

credentials = pika.PlainCredentials(username, password)
params = pika.ConnectionParameters(host, port, '/', credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue=queue)

channel.basic_publish(exchange='', routing_key=queue, body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
