import json
from datetime import date, timedelta
from producers import produce_data, produce_dmz
from utils.dueshit import get_car_maintenance_stuff
from flask import Blueprint, request, render_template, url_for, redirect, flash, session
blueprint = Blueprint('cars', __name__, url_prefix='/cars')


@blueprint.route('/')
def list_cars():
    """
    Display cars list emplate.
    """
    if not session.get('token'):
        return 'Not authed.'

    response = produce_data({
        'action': 'get_cars',
        'token': session.get('token')
    })

    if not response:
        return 'Data was not returned in time.'

    cars = response.get('cars')
    if cars is None:
        cars = []

    return render_template('cars/list.html', cars=cars)


@blueprint.route('/<int:id>')
def display_car(id):
    """
    Display individual car display template.
    """
    if not session.get('token'):
        return 'Not authed.'

    response = produce_data({
        'action': 'get_car',
        'id': id,
        'token': session.get('token')
    })

    if not response:
        return 'Data was not returned in time.'

    return render_template('cars/display.html', car=response.get('car'))


@blueprint.route('/<int:id>/delete', methods=['POST'])
def delete_car(id):
    """
    Delete car from database.
    """
    if not session.get('token'):
        return 'Not authed.'

    response = produce_data({
        'action': 'delete_car',
        'id': id,
        'token': session.get('token')
    })

    if not response:
        return 'Data was not returned in time.'

    if response and response['success'] == True:
        flash('Your car has been deleted!')
    else:
        flash('Your car has NOT been deleted!')

    return redirect(url_for('cars.list_cars'))


@blueprint.route('/<int:id>/update', methods=['POST'])
def update_car(id):
    """
    Update car mileage.
    """
    if not session.get('token'):
        return 'Not authed.'

    response = produce_data({
        'action': 'update_car',
        'id': id,
        'mileage': request.form.get('mileage'),
        'weekly_mileage': request.form.get('weekly_mileage'),
        'token': session.get('token')
    })

    if not response:
        return 'Data was not returned in time.'

    if response and response['success'] == True:
        flash('Your car mileage has been updated!')
    else:
        flash('Your car mileage has NOT been updated!')

    return redirect(url_for('cars.display_car', id=id))


@blueprint.route('/add')
def add_car():
    """
    Display car creation template.
    """
    return render_template('cars/create.html')


@blueprint.route('/add', methods=['POST'])
def add_car_post():
    """
    Process register request.
    """
    make = request.form.get("make")
    model = request.form.get("model")
    year = request.form.get("year")
    mileage = request.form.get("mileage")
    weekly_mileage = request.form.get("weekly_mileage")
    error = None

    if not make:
        error = 'Invalid make.'

    if not model:
        error = 'Invalid model.'

    if not year:
        error = 'Invalid year.'

    response = None
    if not error:
        response = produce_data({
            'action': 'add_car',
            'token': session.get('token'),
            'make': make,
            'model': model,
            'year': year,
            'mileage': mileage,
            'weekly_mileage': weekly_mileage
        })

    if response and response['success'] == True:
        flash('Your car has been added!')
        return redirect(url_for('cars.list_cars'))
    else:
        flash('Your car has NOT been added!')


    return render_template('cars/create.html', error=error)


@blueprint.route('/<int:id>/recalls')
def car_recalls(id):
    """
    Display individual car recalls.
    """
    if not session.get('token'):
        return 'Not authed.'

    db_response = produce_data({
        'action': 'get_car',
        'id': id,
        'token': session.get('token')
    })

    car = db_response.get('car')
    if not car:
        return 'Car does not exist!'

    dmz_response = produce_dmz({
        'action': 'get_recalls',
        'make': car.get('make'),
        'model': car.get('model'),
        'year': car.get('year'),
        'mileage': car.get('mileage'),
        'token': session.get('token')
    })

    results = dmz_response.get('results')

    data = results.get('data')
    if data is None:
        data = []
    return render_template(f'cars/display_recalls.html', car=car, data=data)


@blueprint.route('/<int:id>/maintenance')
def car_maintenance(id):
    """
    Display individual car maintenance.
    """
    if not session.get('token'):
        return 'Not authed.'

    db_response = produce_data({
        'action': 'get_car',
        'id': id,
        'token': session.get('token')
    })

    car = db_response.get('car')
    if not car:
        return 'Car does not exist!'

    data = get_car_maintenance_stuff(car)
    return render_template(f'cars/display_maintenance.html', car=car, data=data)


@blueprint.route('/<int:id>/maintenance', methods=['POST'])
def car_maintenance_post(id):
    """
    Get YouTube video.
    """
    if not session.get('token'):
        return 'Not authed.'

    db_response = produce_data({
        'action': 'get_car',
        'id': id,
        'token': session.get('token')
    })

    car = db_response.get('car')
    if not car:
        return 'Car does not exist!'

    query = request.form.get('query')
    year = car.get('year')
    make = car.get('make')
    model = car.get('model')
    full_query = f'{year} {make} {model} {query}'
    dmz_response = produce_dmz({
        'action': 'youtube_search',
        'query': full_query,
        'token': session.get('token')
    })

    if not dmz_response:
        ez_log('LOG', 'NO_DMZ_RESPONSE_YOUTUBE_SEARCH', full_query)
        return 'No response from DMZ!'

    video_id = None
    try:
        video_id = dmz_response['results'][0]['id']['videoId']
    except:
        return 'No video found!'

    return render_template(
        'cars/display_video.html', car=car, query=query, video_id=video_id
    )


@blueprint.route('/<int:id>/video-playlist')
def video_playlist(id):
    """
    Get YouTube video playlist.
    """
    if not session.get('token'):
        return 'Not authed.'

    db_response = produce_data({
        'action': 'get_car',
        'id': id,
        'token': session.get('token')
    })

    car = db_response.get('car')
    if not car:
        return 'Car does not exist!'

    query = request.form.get('query')
    year = car.get('year')
    make = car.get('make')
    model = car.get('model')
    full_query = f'{year} {make} {model} {query}'
    dmz_response = produce_dmz({
        'action': 'youtube_search',
        'query': full_query,
        'token': session.get('token')
    })

    if not dmz_response:
        ez_log('LOG', 'NO_DMZ_RESPONSE_YOUTUBE_SEARCH', full_query)
        return 'No response from DMZ!'

    videos = []
    for video in dmz_response.get('results', []):
        try:
            videos.append(video['id']['videoId'])
        except:
            pass

    return render_template(
        'cars/display_videos.html', car=car, videos=videos
    )


@blueprint.route('/<int:id>/add-events')
def add_events_to_calendar(id):
    """
    Add events to google calendar.
    """
    if not session.get('token'):
        return 'Not authed.'

    db_response = produce_data({
        'action': 'get_car',
        'id': id,
        'token': session.get('token')
    })

    car = db_response.get('car')
    if not car:
        return 'Car does not exist!'

    dmz_response = produce_dmz({
        'action': 'get_oauth_link'
    })

    if not dmz_response:
        ez_log('LOG', 'NO_DMZ_RESPONSE_ADD_EVENTS', '...')
        return 'No response from DMZ!'

    return render_template(
        'cars/display_add_events.html', car=car, oauth_link=dmz_response.get('results')
    )


@blueprint.route('/<int:id>/add-events', methods=['POST'])
def add_events_to_calendar_post(id):
    """
    Add events to google calendar.
    """
    if not session.get('token'):
        return 'Not authed.'

    db_response = produce_data({
        'action': 'get_car',
        'id': id,
        'token': session.get('token')
    })

    if not response:
        return 'Data was not returned in time.'

    car = db_response.get('car')
    if not car:
        return 'Car does not exist!'

    data = get_car_maintenance_stuff(car)

    if data is None:
        return 'No data received!'

    events = []
    year = car.get('year')
    make = car.get('make')
    model = car.get('model')

    for event in data:
        d = date.strftime(date.today() + timedelta(days=event.get('due_in_days', 0)), '%Y-%m-%d')
        desc = event.get('desc')
        events.append({
            'summary': f'{year} {make} {model}: {desc}',
            'date': d
        })

    dmz_response = produce_dmz({
        'action': 'add_events',
        'oauth_code': request.form.get('oauth_code'),
        'events': events,
    })

    if dmz_response and dmz_response['success'] == True:
        flash('Events have been added to your calendar!')
    else:
        flash('Events have NOT been added to your calendar.')

    return render_template(
        'cars/display_add_events.html',
        car=car, results=dmz_response.get('results')
    )
