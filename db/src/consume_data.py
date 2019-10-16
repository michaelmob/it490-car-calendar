#!/usr/bin/env python3
import os, sys, json
from datetime import date, datetime
from dotenv import load_dotenv; load_dotenv()
from ez import ez_consume
from database import users, cars


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
        return  # Malformed JSON

    # No data means no work to be done
    if not data:
        return

    # Collect values
    action = data.get('action')
    token = data.get('token')
    result = { 'success': True, 'message': 'SUCCESS' }
    user = users.get_by_token(token, 'id')
    user_id = user.get('id')

    if not isinstance(user_id, int):
        print(user_id, type(user_id))
        return

    # Received get_car
    if action == 'get_car':
        result['car'] = cars.get_car(user_id, data.get('id'))

    # Received get_cars
    elif action == 'get_cars':
        result['cars'] = cars.get_cars(user_id)

    # Received create_car
    elif action == 'add_car':
        try:
            result['cars'] = cars.add_car(
                user_id,
                data.get('make'),
                data.get('model'),
                data.get('year'),
                data.get('mileage')
            )
        except Exception as e:
            result['success'] = False
            result['message'] = 'CAR_ADD_ERROR'
            result['exception'] = str(e)

    # Received delete_car request
    elif action == 'delete_car':
        cars.delete_car(user_id, data.get('id'))

    # Unknown action
    else:
        result['success'] = False
        result['message'] = 'UNKNOWN_ACTION'

    return json.dumps(result, default=default)



if __name__ == '__main__':
    ez_consume('DATA', 'data-queue-rpc', callback)
