#!/usr/bin/env python3
import os, json, requests, html
import youtube, carmd
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
    DMZ consumer callback.
    """
    try:
        data = json.loads(body)
    except Exception as e:
        return  # Malformed JSON

    # No data? No idea.
    if not data:
        return

    car_md_args = lambda d: (
        d.get('make'), d.get('model'), d.get('year'), d.get('mileage')
    )

    action = data.get('action')
    result = { 'success': True }

    # Received youtube search request
    if action == 'youtube_search':
        result['results'] = youtube.search(data.get('query'))

    # Received car maintence request
    elif action == 'get_maintenance':
        result['results'] = carmd.get_maintenance(*car_md_args(data))

    # Received car recalls request
    elif action == 'get_recalls':
        result['results'] = carmd.get_recalls(*car_md_args(data))

    # Unknown action
    else:
        result['success'] = False

    return json.dumps(result, default=default)


if __name__ == '__main__':
    ez_consume('DMZ', 'dmz-queue-rpc', callback)
