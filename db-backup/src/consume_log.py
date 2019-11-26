#!/usr/bin/env python3
import os, sys, json
from dotenv import load_dotenv; load_dotenv()
from ez import logger, ez_consume


def callback(ch, method, properties, body):
    """
    Write 'body' contents to a log file.
    """
    try:
        data = json.loads(body)
    except Exception as e:
        return  # Malformed JSON

    if not isinstance(data, dict):
        return

    logger.write_log(data.get('message_type', 'LOG'), str(data.get('message')))


if __name__ == '__main__':
    ez_consume('LOG', 'log-queue', callback)
