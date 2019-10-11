import json
from producers import produce_auth
from flask import Blueprint, request, render_template

blueprint = Blueprint('auth', __name__, url_prefix='/auth')


@blueprint.route('/register')
def register():
    """
    Display register template.
    """
    return render_template('register.html')


@blueprint.route('/register', methods=['POST'])
def register_post():
    """
    Process register request.
    """
    email = request.form["email"]
    username = request.form["username"]
    password = request.form["password"]

    if not username:
        return 'Invalid username.'

    if not password:
        return 'Invalid password.'

    response = produce_auth({
        'action': 'register',
        'email': email,
        'username': username,
        'password': password
    })
    return 'Registered!'


@blueprint.route('/login')
def login():
    """
    Display login template.
    """
    return render_template('login.html')


@blueprint.route('/login', methods=['POST'])
def login_post():
    """
    Process login request.
    """
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return redirect(url_for('index'))

    response = produce_auth({
        'action': 'login',
        'username': username,
        'password': password
    })

    if response and response['success'] == True:
        flash('You were successfully logged in')
        return redirect(url_for('index'))
    else:
        return render_template('login.html', error='Invalid credentials.')
