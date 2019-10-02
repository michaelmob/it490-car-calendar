#!/usr/bin/env python3
import os
import os.path
import pika
from datetime import datetime, date



class Logger:
    """
    Logging system.
    """

    def __init__(self, path: str):
        """
        Set path and create path directory if non-existant.
        """
        self.path = path

        # Create path
        if not os.path.exists(path):
            os.mkdir(path)

        # Ensure access to log path
        if not os.access(path, os.W_OK):
            raise PermissionError()


    def get_log_filename(self):
        """
        Get the file name of the log file.
        This method does not create the log file.
        """
        return os.path.join(self.path, str(date.today()) + '.log')


    def format_message(self, message_type: str, message: str):
        """
        Create formatted message based on message type and content.
        """
        return f'[{datetime.now()}] {message_type}: {message}\n'


    def write_log(self, message_type: str, message: str):
        """
        Write message to log file.
        """
        with open(self.get_log_filename(), 'a+') as f:
            f.write(self.format_message(message_type, message))


# TODO: Move Consumer to a new file. Add optional callback.
class Consumer:
    """
    Log queue consumer.
    """

    def __init__(self, host, port, vhost, username, password):
        """
        Initialize LogConsumer.
        """
        credentials = pika.PlainCredentials(username, password)
        params = pika.ConnectionParameters(host, port, vhost, credentials)
        connection = pika.BlockingConnection(params)
        self.channel = connection.channel()


    def consume(self, queue):
        """
        Consuming listener.
        """
        self.channel.queue_declare(queue=queue)
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=queue, on_message_callback=self.callback)
        print('[*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()


    def callback(self, ch, method, properties, body):
        """
        Consume into callback.
        """
        if self.logger is not None:
            self.logger.write_log('LOG', body)

        print("[x] Received %r" % body)
        print("[x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)



if __name__ == '__main__':
    # Config
    # TODO: Use environment variables
    host = ''
    port = 5672
    queue = 'log-queue'
    username = 'log'
    password = 'logpass'
    log_path = '/var/log/car-calendar'

    # Run
    consumer = Consumer(host, port, '/', username, password)
    consumer.logger = Logger(log_path)
    consumer.consume(queue)
