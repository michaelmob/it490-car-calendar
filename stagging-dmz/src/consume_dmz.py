#!/usr/bin/env python3
import os, json, requests, html
import youtube, carmd, google_calendar
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
        try:
            result['results'] = youtube.search(data.get('query'))
            raise 'www'
        except Exception as e:
            result['success'] = False
            ez_log('LOG', 'YOUTUBE_SEARCH', str(e))

    # Received car maintence request
    elif action == 'get_maintenance':
        try:
            result['results'] = carmd.get_maintenance(*car_md_args(data))
            if result['results']['message'].get('code') == 1003:
                ez_log('LOG', 'CARMD_API_OUT_OF_CREDITS', 'Maintenance')
        except Exception as e:
            result['success'] = False
            ez_log('LOG', 'GET_MAINTENANCE', str(e))

    # Received car recalls request
    elif action == 'get_recalls':
        try:
            result['results'] = carmd.get_recalls(*car_md_args(data))
            if result['results']['message'].get('code') == 1003:
                ez_log('LOG', 'CARMD_API_OUT_OF_CREDITS', 'Recalls')
        except Exception as e:
            result['success'] = False
            ez_log('LOG', 'GET_RECALLS', str(e))

    # Received oauth link request
    elif action == 'get_oauth_link':
        try:
            result['results'] = google_calendar.get_oauth_link()
        except Exception as e:
            result['success'] = False
            ez_log('LOG', 'GET_OAUTH_LINK', str(e))

    # Received oauth link request
    elif action == 'add_events':
        oauth_code = data.get('oauth_code')
        events = data.get('events')
        try:
            result['results'] = google_calendar.add_events(oauth_code, events)
        except Exception as e:
            result['success'] = False
            ez_log('LOG', 'ADD_EVENTS', str(e))

    # Unknown action
    else:
        result['success'] = False

    return json.dumps(result, default=default)


if __name__ == '__main__':
    ez_consume('DMZ', 'dmz-queue-rpc', callback)
