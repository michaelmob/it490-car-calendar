import json
from producers import produce_auth
from flask import Blueprint, request, render_template, url_for, redirect, flash

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
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    error = None

    if not username:
        error = 'Invalid username.'

    if not password:
        error = 'Invalid password.'

    if not email:
        error = 'Invalid email.'

    if password != confirm_password:
        error = 'Passwords do not match.'

    response = None
    if not error:
        response = produce_auth({
            'action': 'register',
            'email': email,
            'username': username,
            'password': password
        })

    if response and response['success'] == True:
        flash('You have registered. Please log in now.')
        return redirect(url_for('auth.login'))

    return render_template('register.html', error=error)


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
    error = None
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        error = ''

    response = None
    if not error:
        response = produce_auth({
            'action': 'login',
            'username': username,
            'password': password
        })

    if response and response['success'] == True:
        flash('Welcome %s!', (username,))
        return redirect(url_for('general.index'))
    else:
        error = 'Invalid credentials.'

    return render_template('login.html', error=error)
