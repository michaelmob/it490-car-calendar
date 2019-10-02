#!/usr/bin/env python3
from consumer import Consumer
from logger import Logger


if __name__ == '__main__':
    # Config
    # TODO: Use environment variables
    host = ''
    port = 5672
    queue = 'log-queue'
    username = 'log'
    password = 'logpass'
    log_path = '/var/log/car-calendar'
    logger = Logger(log_path)

    def callback(ch, method, properties, body):
        logger.write_log('LOG', str(body))

    # Run
    consumer = Consumer(host, port, '/', username, password)
    consumer.consume(queue, callback=callback)
