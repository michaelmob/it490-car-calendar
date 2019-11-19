#!/usr/bin/env python3
import os, sys, json
from datetime import date, datetime
from dotenv import load_dotenv; load_dotenv()
from ez import ez_consume, ez_log
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
    id = data.get('id')

    result = { 'success': True, 'message': 'SUCCESS' }
    try:
        user = users.get_by_token(token, 'id')
    except Exception as e:
        result['success'] = False
        result['message'] = 'USER_GET_ERROR'
        ez_log('LOG', result['message'], f'Token: {token} ({str(e)})')
        result['exception'] = str(e)
        return result

    if not isinstance(user, dict):
        result['success'] = False
        result['message'] = 'USER_NOT_FOUND'
        ez_log('LOG', result['message'], f'Token: {token}')
        return result

    user_id = user.get('id')

    # Received get_car
    if action == 'get_car':
        try:
            result['car'] = cars.get_car(user_id, data.get('id'))
        except Exception as e:
            result['success'] = False
            result['message'] = 'CAR_GET_ERROR'
            result['exception'] = str(e)
            ez_log('LOG', result['message'], f'Token: {token} ({str(e)}), ID: {id}')
            return result

    # Received get_cars
    elif action == 'get_cars':
        try:
            result['cars'] = cars.get_cars(user_id)
        except Exception as e:
            result['success'] = False
            result['message'] = 'CARS_GET_ERROR'
            ez_log('LOG', result['message'], f'Token: {token} ({str(e)})')
            result['exception'] = str(e)

    # Received create_car
    elif action == 'add_car':
        try:
            result['cars'] = cars.add_car(
                user_id,
                data.get('make'),
                data.get('model'),
                data.get('year'),
                data.get('mileage'),
                data.get('weekly_mileage')
            )
        except Exception as e:
            result['success'] = False
            result['message'] = 'CAR_ADD_ERROR'
            result['exception'] = str(e)
            ez_log('LOG', result['message'], f'Token: {token} ({str(e)})')
            return result

    # Received delete_car request
    elif action == 'delete_car':
        try:
            cars.delete_car(user_id, data.get('id'))
        except Exception as e:
            result['success'] = False
            result['message'] = 'CAR_DELETE_ERROR'
            result['exception'] = str(e)
            ez_log('LOG', result['message'], f'Token: {token} ({str(e)}), ID: {id}')
            return result

    # Received update_car request
    elif action == 'update_car' and data.get('mileage'):
        try:
            cars.update_car(
                data.get('id'), data.get('mileage'), data.get('weekly_mileage')
            )
        except Exception as e:
            result['success'] = False
            result['message'] = 'CAR_UPDATE_ERROR'
            result['exception'] = str(e)
            ez_log('LOG', result['message'], f'Token: {token} ({str(e)}), ID: {id}')
            return result

    # Unknown action
    else:
        result['success'] = False
        result['message'] = 'UNKNOWN_ACTION'
        ez_log('LOG', result['message'], f'Token: {token}')

    return json.dumps(result, default=default)



if __name__ == '__main__':
    ez_consume('DATA', 'data-queue-rpc', callback)
