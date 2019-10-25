#!/usr/bin/env python3
import os, json, requests, html
import youtube
from dotenv import load_dotenv; load_dotenv()
from datetime import date, datetime
from ez import ez_consume, ez_log


def default(value):
    """
    Convert date/times to strings. Fixes 'datetime not JSON serializable'.
    """
    if isinstance(value, date) or isinstance(value, datetime):
        return value.isoformat()


def callback(ch, method, props, body):
    """
    YouTube search request callback.
    """
    try:
        data = json.loads(body)
    except Exception as e:
        return  # Malformed JSON

    if not data:
        return

    action = data.get('action')
    result = { 'success': False }

    # Received search attempt
    if action == 'search':
        result['results'] = youtube.search(data.get('query'))

    return json.dumps(result, default=default)


if __name__ == '__main__':
    ez_consume('DMZ', 'dmz-queue-rpc', callback)
