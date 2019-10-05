#!/usr/bin/env python3
import os
import dotenv
from consumers.auth_consumer import AuthConsumer  # pylint: disable=import-error
from dotenv import load_dotenv


def callback(ch, method, props, body):
    """

    """
    print('Received:', body)


def main():
    """

    """
    load_dotenv(os.getenv('AUTH_ENV', '.env_auth'))  # Load .env file

    # Start consuming
    auth_consumer = AuthConsumer(
        host=os.getenv('RABBITMQ_HOST'),
        port=int(os.getenv('RABBITMQ_PORT', 5672)),
        vhost=os.getenv('RABBITMQ_VHOST'),
        username=os.getenv('RABBITMQ_USER'),
        password=os.getenv('RABBITMQ_PASS')
    )

    auth_consumer.consume(
        queue=os.getenv('RABBITMQ_QUEUE', 'auth-queue-rpc'),
        callback=callback
    )


if __name__ == '__main__':
    main()
