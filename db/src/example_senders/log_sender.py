# import os, json
# from dotenv import load_dotenv  # Load environment variables from env file first
# load_dotenv(os.getenv('AUTH_ENV', '../.env_log'))
#
# import pika
#
# host = str(os.getenv('RABBITMQ_HOST'))
# port = int(os.getenv('RABBITMQ_PORT', 5672))
# queue = os.getenv('RABBITMQ_QUEUE', 'log-queue')
# username = os.getenv('RABBITMQ_LOG_USER')
# password = os.getenv('RABBITMQ_LOG_PASS')
#
# credentials = pika.PlainCredentials(username, password)
# params = pika.ConnectionParameters(host, port, '/', credentials)
# connection = pika.BlockingConnection(params)
# channel = connection.channel()
#
# channel.queue_declare(queue=queue)
#
# channel.basic_publish(exchange='', routing_key=queue, body=json.dumps({
#     'message_type': 'TEST',
#     'message': 'This is a test log.'
# }))
# print(" [x] Sent 'Hello World!'")
# connection.close()

# Above is condensed to below with ez_log
# You must have the environment vars set by sourcing .env
from ez import ez_log
ez_log('LOG', 'TEST', 'This is a test log.')
