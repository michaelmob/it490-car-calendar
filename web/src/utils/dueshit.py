from producers import produce_dmz


def get_car_maintenance_stuff(car):
    dmz_response = produce_dmz({
        'action': 'get_maintenance',
        'make': car.get('make'),
        'model': car.get('model'),
        'year': car.get('year'),
        'mileage': car.get('mileage'),
    })

    daily_mileage = int(car.get('weekly_mileage')) / 7
    if not dmz_response.get('results'):
        return []

    data = dmz_response['results'].get('data')
    if data is None:
        return []

    for result in data:
        if 'due_mileage' not in result:
            continue

        car_mileage = int(car['mileage'])
        due_mileage = int(result['due_mileage'])

        # there's a formula for this
        s = 0
        while s < car_mileage:
            s += due_mileage

        result['due_in_miles'] = abs(car_mileage - s)
        result['due_in_days'] = int(result['due_in_miles'] / daily_mileage)

    return data
