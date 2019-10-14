#!/usr/bin/env python3
import os, sys, json
from datetime import date, datetime
from dotenv import load_dotenv; load_dotenv()
from helpers import logger, ez_consume, ez_produce
from database.cars import Car


def default(value):
    """
    Convert date/times to strings. Fixes 'datetime not JSON serializable'.
    """
    if isinstance(value, date) or isinstance(value, datetime):
        return value.isoformat()


def callback(ch, method, props, body):
    """
    Auth callback that is called when an auth attempt occurs.
    """
    try:
        data = json.loads(body)
    except:
        print('malformed')
        return  # Malformed JSON

    if not data:
        return

    action = data.get('action')
    token = data.get('token')
    result = { 'success': True }

    # Received get_car
    if action == 'get_car':
        result['car'] = Car.get_car(token, data.get('id'))

    # Received get_cars
    elif action == 'get_cars':
        result['cars'] = Car.get_cars(token)

    # Received create_car
    elif action == 'add_car':
        result['cars'] = Car.add_car(
            token,
            data.get('make'),
            data.get('model'),
            data.get('year'),
            data.get('mileage')
        )

    # Received delete_car request
    elif action == 'delete_car':
        Car.delete_car(token, data.get('id'))

    # Unknown action
    else:
        result['success'] = False
        result['message'] = 'unknown_action'

    return json.dumps(result, default=default)


if __name__ == '__main__':
    ez_consume('DATA', 'data-queue-rpc', callback)
