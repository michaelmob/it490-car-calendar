#!/usr/bin/env python3
import os
from dotenv import load_dotenv  # Load environment variables from env file first
load_dotenv(os.getenv('AUTH_ENV', '.env_auth'))

import json
from amqp.consumer import Consumer  # pylint: disable=import-error
from database.auth import Auth  # pylint: disable=import-error


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
    # Start consuming
    auth_consumer = Consumer(
        host=os.getenv('RABBITMQ_HOST'),
        port=int(os.getenv('RABBITMQ_PORT', 5672)),
        vhost=os.getenv('RABBITMQ_VHOST', '/'),
        username=os.getenv('RABBITMQ_USER'),
        password=os.getenv('RABBITMQ_PASS')
    )
    print('[*] Waiting for auth messages. To exit press CTRL+C')
    auth_consumer.consume(
        queue=os.getenv('RABBITMQ_QUEUE', 'auth-queue-rpc'),
        callback=callback
    )


if __name__ == '__main__':
    main()
