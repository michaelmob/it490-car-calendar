import os
import json
from producer import Producer
from logger import Logger

logger = Logger(os.getenv('LOG_PATH', '/var/log/car-calendar'))


def ez_produce(name, queue, data, is_rpc=False):
    """
    Send data to queue.
    """
    if not (name and queue and data):
        return

    name = name.upper()
    try:
        producer = Producer(
            host=os.getenv('RABBITMQ_HOST'),
            port=os.getenv('RABBITMQ_PORT', 5672),
            vhost=os.getenv('RABBITMQ_VHOST', '/'),
            username=os.getenv('RABBITMQ_%s_USER' % name),
            password=os.getenv('RABBITMQ_%s_PASS' % name),
            is_rpc=True
        )

        response = json.loads(producer.produce(
            queue=os.getenv('RABBITMQ_%s_QUEUE' % name, queue),
            value=json.dumps(data)
        ))
    except Exception as e:
        print(e)
        logger.write_log('%s_CONSUMER_ERROR' % name, e)
        return False

    # Sometimes, the first json.loads returns a string...
    if isinstance(response, str):
        response = json.loads(response)

    if is_rpc:
        return response

    return True


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

    if not response:
        return

    # I'm so sorry, but the first loads returns a str insead of a
    # dict for some reason
    return json.loads(json.loads(response))


def produce_data(data):
    """
    Data producer helper function.
    """
    response = ez_produce('DATA', 'data-queue-rpc', data, True)
    return response


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


def get_user(token: str):
    """
    Get user by token.
    """
    return produce_auth({ 'action': 'get_user', 'token': token })
