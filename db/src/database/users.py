from database.db import db
from uuid import uuid4
from hashlib import sha1



whitelist_fields = (
    'id', 'username', 'email', 'first_name', 'last_name', 'token'
)


def get_by_username_or_email(username_or_email: str, fields='*'):
    """
    Fetch user by its username or email address.
    Returns user dict or None.
    """
    if not username_or_email:
        return

    field = 'username'
    if '@' in username_or_email:
        field = 'email'

    query = "SELECT {} FROM `users` WHERE {}=%s".format(fields, field)
    db.execute(query, (username_or_email,))
    return db.fetchone()


def get_by_token(token: str, fields='*'):
    """
    Fetch user by its token.
    Returns user dict or None.
    """
    if not token:
        return

    query = "SELECT {} FROM `users` WHERE token=%s LIMIT 1".format(fields)
    db.execute(query, (token,))
    return db.fetchone()


def token_to_user_id(token: str, fields='*'):
    """
    Retrieve users id from their token.
    """
    return get_by_token(token, 'id')


def is_token_taken(token: str):
    """
    Test if token is already taken.
    Returns true if token is taken.
    """
    if not token:
        return

    query = "SELECT EXISTS(SELECT 1 FROM `users` WHERE token=%s) AS taken;"
    db.execute(query, (token,))
    return db.fetchone().get('taken') == 1


def generate_token():
    """
    Generate a user token. This does not update the column.
    """
    token = None
    while not token:
        token = sha1(uuid4().urn.encode('utf-8')).hexdigest()
        if is_token_taken(token):
            token = None
    return token
