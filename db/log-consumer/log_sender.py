#!/usr/bin/env python3
import pika

credentials = pika.PlainCredentials('', '')
params = pika.ConnectionParameters('', 5672, '/', credentials)
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='log-queue')

channel.basic_publish(exchange='', routing_key='log-queue', body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()
