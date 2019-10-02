#!/usr/bin/env python3
import os
from consumer import Consumer
from logger import Logger


if __name__ == '__main__':
    # Config
    # TODO: Use environment variables
    host = str(os.getenv('RABBITMQ_HOST'))
    port = int(os.getenv('RABBITMQ_PORT', 5672))
    queue = os.getenv('RABBITMQ_QUEUE', 'log-queue')
    username = os.getenv('RABBITMQ_USER', 'log')
    password = os.getenv('RABBITMQ_PASS', 'logpass')
    logger = Logger(os.getenv('LOG_PATH', '/var/log/car-calendar'))

    def callback(ch, method, properties, body):
        logger.write_log('LOG', str(body))

    # Run
    consumer = Consumer(host, port, '/', username, password)
    consumer.consume(queue, callback=callback)
