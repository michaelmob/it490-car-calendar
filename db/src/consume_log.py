#!/usr/bin/env python3
import os
from consumer import Consumer
from logger import Logger


# Logger and its callback
logger = Logger(os.getenv('LOG_PATH', '/var/log/car-calendar'))

def callback(ch, method, properties, body):
    """
    Write 'body' contents to a log file.
    """
    logger.write_log('LOG', str(body))

consumer = Consumer(
    host=str(os.getenv('RABBITMQ_HOST')),
    port=int(os.getenv('RABBITMQ_PORT', 5672)),
    vhost='/',
    username=os.getenv('RABBITMQ_USER', 'log'),
    password=os.getenv('RABBITMQ_PASS', 'logpass')
)

consumer.consume(
    queue=os.getenv('RABBITMQ_QUEUE', 'log-queue'),
    callback=callback
)
