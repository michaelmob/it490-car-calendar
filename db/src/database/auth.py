from uuid import uuid4
from hashlib import sha1, sha256
from database.db import db, conn
from MySQLdb._exceptions import IntegrityError
from database import users



def register(username, email, password, first_name, last_name):
    """
    Register a new user account.
    """
    message = lambda m, s=False: { 'message': m, 'success': s }

    # Validate arguments
    if not username:
        return message('EMPTY_USERNAME')

    if '@' in username:
        return message('USERNAME_IS_EMAIL')

    if not email:
        return message('EMPTY_EMAIL')

    if not password:
        return message('EMPTY_PASSWORD')

    # Generate random salt and token
    encode = lambda x: x.encode('utf-8')
    salt = sha1(encode(uuid4().urn)).hexdigest()
    password = sha256(encode(password) + encode(salt)).hexdigest()
    token = users.generate_token()

    # Build and execute new user query
    query = """
        INSERT INTO `users` (
            `username`, `email`, `password`, `salt`,
            `first_name`, `last_name`, `token`
        ) VALUES (%s,%s,%s,%s,%s,%s,%s);"""

    try:
        db.execute(query, (
            username, email, password, salt, first_name, last_name, token
        ))
        conn.commit()
        return message('USER_CREATED', True)

    # Constraint should stop non-unique usernames or emails.
    except IntegrityError:
        return message('USER_EXISTS', False)


def login(username_or_email, password):
    """
    Attempt to log a user in.
    Returns an API token.
    """
    if not (username_or_email and password):
        return

    user = users.get_by_username_or_email(username_or_email)

    # Get hashed password if user exists
    if user:
        hashed_password = sha256(
            str(password + user['salt']).encode('utf-8')).hexdigest()

    # But if user doesn't exist (we won't need the hashed_password), or the
    # users password isnt a match... deny them
    if not user or (user and user.get('password') != hashed_password):
        return { 'message': 'USER_DOES_NOT_EXIST', 'success': False }

    # Return user data
    return {
        'user': {
            key: user[key] for key in user
                if key in users.whitelist_fields
        },
        'message': 'LOGIN_SUCCESS',
        'success': True
    }
