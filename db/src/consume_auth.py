#!/usr/bin/env python3
import os
from dotenv import load_dotenv  # Load environment variables from env file first
load_dotenv(os.getenv('ENV_FILE', '.env_auth'))

import sys
import json
from consumer import Consumer
from producer import Producer
from database.auth import Auth


def produce_log(log_type, message):
    """
    Produce log to the log queue.
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
        return False

    producer.produce(
        os.getenv('RABBITMQ_LOG_QUEUE', 'log-queue'),
        json.dumps({ 'type': log_type, 'message': message })
    )
    return True


def callback(ch, method, props, body):
    """
    Auth callback that is called when an auth attempt occurs.
    """
    try:
        data = json.loads(body)
    except:
        return  # Malformed JSON

    if not data:
        return

    action = data.get('action')
    result = { 'success': False }

    # Received login attempt
    if action == 'login':
        result = Auth.login(
            username_or_email=data.get('username') or data.get('email'),
            password=data.get('password')
        )

    # Received registration attempt
    elif action == 'register':
        result = Auth.register(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name')
        )

    else:
        result['message'] = 'Unknown action.'

    return json.dumps(result)


def main():
    """
    Start auth consumer.
    """
    auth_consumer = None
    try:
        # Start consuming
        auth_consumer = Consumer(
            host=os.getenv('RABBITMQ_HOST'),
            port=int(os.getenv('RABBITMQ_PORT', 5672)),
            vhost=os.getenv('RABBITMQ_VHOST', '/'),
            username=os.getenv('RABBITMQ_AUTH_USER'),
            password=os.getenv('RABBITMQ_AUTH_PASS')
        )
    except Exception as e:
        print(e)
        args = ('AUTH_CONSUMER_ERROR', e)
        logger.write_log(*args)
        produce_log(*args)
        sys.exit(1)

    print('[*] Waiting for auth messages. To exit press CTRL+C')
    auth_consumer.consume(
        queue=os.getenv('RABBITMQ_AUTH_QUEUE', 'auth-queue-rpc'),
        callback=callback
    )


if __name__ == '__main__':
    main()
