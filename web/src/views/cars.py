import json
from producers import produce_data, produce_dmz
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

    return render_template('cars/list.html', cars=response.get('cars'))


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

    return render_template('cars/display.html', car=response.get('car'))


@blueprint.route('/<int:id>/delete', methods=['POST'])
def delete_car(id):
    """
    Display individual car display template.
    """
    if not session.get('token'):
        return 'Not authed.'

    response = produce_data({
        'action': 'delete_car',
        'id': id,
        'token': session.get('token')
    })

    if response and response['success'] == True:
        flash('Your car has been deleted!')
    else:
        flash('Your car has NOT been deleted!')

    return redirect(url_for('cars.list_cars'))


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
            'mileage': mileage
        })

    if response and response['success'] == True:
        flash('Your car has been added!')
        return redirect(url_for('cars.list_cars'))

    return render_template('cars/create.html', error=error)


def car_generic(id, action):
    """
    Generic car fetch info from dmz.
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
        'action': 'get_' + action,
        'make': car.get('make'),
        'model': car.get('model'),
        'year': car.get('year'),
        'mileage': car.get('mileage'),
        'token': session.get('token')
    })

    results = dmz_response.get('results')

    return render_template(
        f'cars/display_{action}.html',
        car=car, data=results.get('data') if results else []
    )


@blueprint.route('/<int:id>/recalls')
def car_recalls(id):
    """
    Display individual car recalls.
    """
    return car_generic(id, 'recalls')


@blueprint.route('/<int:id>/maintenance')
def car_maintenance(id):
    """
    Display individual car maintenance.
    """
    return car_generic(id, 'maintenance')
