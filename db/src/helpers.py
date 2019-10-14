import os
from consumer import Consumer
from producer import Producer
from logger import Logger

logger = Logger(os.getenv('LOG_FILE', '/var/log/car-calendar'))


def ez_produce(name, queue, data, is_rpc=False):
    """
    Send data to queue.
    """
    name = name.upper()
    try:
        producer = Producer(
            host=os.getenv('RABBITMQ_HOST'),
            port=os.getenv('RABBITMQ_PORT', 5672),
            vhost=os.getenv('RABBITMQ_VHOST', '/'),
            username=os.getenv('RABBITMQ_%s_USER' % name),
            password=os.getenv('RABBITMQ_%s_PASS' % name)
        )
    except Exception as e:
        print(e)
        logger.write_log('%s_CONSUMER_ERROR' % name, e)
        return False

    response = producer.produce(
        queue=os.getenv('RABBITMQ_%s_QUEUE' % name, queue),
        value=json.dumps(data)
    )

    if is_rpc:
        return response

    return True


def ez_consume(name, queue, callback):
    """
    Receive data from queue.
    """
    name = name.upper()
    consumer = None
    try:
        # Start consuming
        consumer = Consumer(
            host=os.getenv('RABBITMQ_HOST'),
            port=int(os.getenv('RABBITMQ_PORT', 5672)),
            vhost=os.getenv('RABBITMQ_VHOST', '/'),
            username=os.getenv('RABBITMQ_%s_USER' % name),
            password=os.getenv('RABBITMQ_%s_PASS' % name)
        )
    except Exception as e:
        raise e
        logger.write_log('%s_CONSUMER_ERROR' % name, e)
        return False

    print('[*] Waiting for %s messages. To exit press CTRL+C' % queue)
    consumer.consume(
        queue=os.getenv('RABBITMQ_%s_QUEUE' % name, queue),
        callback=callback
    )
    return True
