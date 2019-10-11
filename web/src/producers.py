import os
import json
from producer import Producer
from logger import Logger

logger = Logger(os.getenv('LOG_PATH', '/var/log/car-calendar'))


def produce_auth(data):
    """
    Auth producer helper function.
    """
    try:
        producer = Producer(
            host=os.getenv('RABBITMQ_HOST'),
            port=os.getenv('RABBITMQ_PORT', 5672),
            vhost=os.getenv('RABBITMQ_VHOST', '/'),
            username=os.getenv('RABBITMQ_AUTH_USER'),
            password=os.getenv('RABBITMQ_AUTH_PASS'),
            is_rpc=True
        )
    except Exception as e:
        print(e)
        logger.write_log('AUTH_PRODUCER_ERROR', e)
        return

    response = producer.produce(
        os.getenv('RABBITMQ_AUTH_QUEUE', 'auth-queue-rpc'),
        json.dumps(data)
    )

    # I'm so sorry, but the first loads returns a str insead of a
    # dict for some reason
    return json.loads(json.loads(response))


def produce_log(log_type, message):
    """
    Log producer helper function.
    """
    try:
        producer = Producer(
            host=os.getenv('RABBITMQ_HOST'),
            port=os.getenv('RABBITMQ_PORT', 5672),
            vhost=os.getenv('RABBITMQ_VHOST', '/'),
            username=os.getenv('RABBITMQ_LOG_USER'),
            password=os.getenv('RABBITMQ_LOG_PASS')
        )
    except Exception as e:
        print(e)
        logger.write_log('LOG_PRODUCER_ERROR', e)
        return

    producer.produce(
        os.getenv('RABBITMQ_LOG_QUEUE', 'log-queue'),
        json.dumps(data)
    )
