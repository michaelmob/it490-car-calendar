#!/usr/bin/env python3
import os
from dotenv import load_dotenv  # Load environment variables from env file first
load_dotenv(os.getenv('AUTH_ENV', '.env_log'))

import json
from consumer import Consumer
from logger import Logger

# Logger and its callback
logger = Logger(os.getenv('LOG_PATH', '/var/log/car-calendar'))

def callback(ch, method, properties, body):
    """
    Write 'body' contents to a log file.
    """
    data = json.loads(body)
    logger.write_log(
        data.get('type', 'LOG'),
        str(body.get('message'))
    )

consumer = Consumer(
    host=str(os.getenv('RABBITMQ_HOST')),
    port=int(os.getenv('RABBITMQ_PORT', 5672)),
    vhost=os.getenv('RABBITMQ_VHOST', '/'),
    username=os.getenv('RABBITMQ_USER'),
    password=os.getenv('RABBITMQ_PASS')
)

print('[*] Waiting for log messages. To exit press CTRL+C')

consumer.consume(
    queue=os.getenv('RABBITMQ_QUEUE', 'log-queue'),
    callback=callback
)
