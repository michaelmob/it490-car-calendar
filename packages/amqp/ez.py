import os, json
from consumer import Consumer
from producer import Producer
from logger import Logger

logger = Logger(os.getenv('LOG_FILE', '/var/log/car-calendar'))


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
            is_rpc=is_rpc
        )
        response = json.loads(producer.produce(
            queue=os.getenv('RABBITMQ_%s_QUEUE' % name, queue),
            value=json.dumps(data)
        ))
    except AttributeError as e:
        message = 'Your .env file is probably not set up correctly.'
        print({
            'MESSAGE': message,
            'NAME': name,
            'QUEUE': queue,
            'RABBITMQ_HOST': os.getenv('RABBITMQ_HOST'),
            'RABBITMQ_PORT': os.getenv('RABBITMQ_PORT', 5672),
            'RABBITMQ_VHOST': os.getenv('RABBITMQ_VHOST', '/'),
            'RABBITMQ_%s_USER': os.getenv('RABBITMQ_%s_USER' % name),
            'RABBITMQ_%s_PASS': os.getenv('RABBITMQ_%s_PASS' % name),
        })
        logger.write_log('%s_PRODUCER_ERROR' % name, message)
    except Exception as e:
        if is_rpc:
            raise e
        else:
            logger.write_log('%s_PRODUCER_ERROR' % name, e)
            return False

    # Sometimes, the first json.loads returns a string...
    if isinstance(response, str):
        response = json.loads(response)

    return response if is_rpc else True


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
        logger.write_log('%s_CONSUMER_ERROR' % name, e)
        raise e

    print('[*] Waiting for %s messages. To exit press CTRL+C' % queue)
    consumer.consume(
        queue=os.getenv('RABBITMQ_%s_QUEUE' % name, queue),
        callback=callback
    )
    return True


def ez_log(name, message_type, message):
    """
    Produce log to amqp broker and write to local log.
    """
    # Local Write
    logger.write_log(message_type, message)

    # External Write
    data = { 'message_type': message_type, 'message': message }
    ez_produce(name, os.getenv('RABBITMQ_LOG_QUEUE', 'log-queue'), data)
