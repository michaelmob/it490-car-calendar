import os, json
from consumer import Consumer
from producer import Producer
from logger import Logger

logger = Logger(os.getenv('LOG_FILE', '/home/vagrant/logs'))


def ez_produce(name, queue, data, is_rpc=False, rpc_attempts=25):
    """
    Send data to queue.
    """
    if not (name and queue and data and isinstance(data, dict)):
        return

    name = name.upper()

    if not data:
        return False

    try:
        producer = Producer(
            host=os.getenv('RABBITMQ_HOST'),
            port=os.getenv('RABBITMQ_PORT', 5672),
            vhost=os.getenv('RABBITMQ_VHOST', '/'),
            username=os.getenv('RABBITMQ_%s_USER' % name),
            password=os.getenv('RABBITMQ_%s_PASS' % name),
            is_rpc=is_rpc,
            rpc_attempts=rpc_attempts
        )

        response = producer.produce(
            queue=os.getenv('RABBITMQ_%s_QUEUE' % name, queue),
            value=json.dumps(data)
        )

        # This MUST be ran through json.loads again...
        if response:
            response = json.loads(response)

    # Couldn't connect to rabbitmq, most likely
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
        logger.write_log('%s_PRODUCER_ERROR_ATTR_ERROR' % name, message)
        return False

    # Type errors happen when data cannot be serialized to JSON
    except TypeError as e:
        logger.write_log('%s_PRODUCER_ERROR_TYPE_ERROR' % name, str(e))
        return False

    # Any other exception
    except Exception as e:
        if is_rpc:
            raise e
        else:
            logger.write_log('%s_PRODUCER_ERROR' % name, str(e))
            return False

    if not is_rpc:
        return True

    if response:
        return json.loads(response) if isinstance(response, str) else response


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

    `name` argument is now unneeded.
    """
    # Local Write
    logger.write_log(message_type, message)

    # External Write
    data = { 'message_type': message_type, 'message': message }
    ez_produce('LOG', os.getenv('RABBITMQ_LOG_QUEUE', 'log-queue'), data)
