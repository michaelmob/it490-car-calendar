from uuid import uuid4
from hashlib import sha1, sha256
from database.db import db, conn
from MySQLdb._exceptions import IntegrityError


class Auth:
    """
    Authentication and authorization.
    """

    @staticmethod
    def register(username, email, password, first_name, last_name):
        """
        Register a new user account.
        """
        message = lambda m, s=False: { 'message': m, 'success': s }

        # Validate arguments
        if not username:
            return message('Username cannot be empty.')

        if '@' in username:
            return message('Username cannot contain a \'@\'.')

        if not email:
            return message('Email cannot be empty.')

        if not password:
            return message('Password cannot be empty.')


        # Generate random salt and token
        encode = lambda x: x.encode('utf-8')
        token = sha1(encode(uuid4().urn)).hexdigest()
        salt = sha1(encode(uuid4().urn)).hexdigest()
        password = sha256(encode(password) + encode(salt)).hexdigest()

        # TODO: Check to see if token isn't taken, otherwise, on
        # register a user may be told that an account already exists
        # with their username/email but its the token thats already
        # taken.

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
            return message('User created!', True)

        # Constraint should stop non-unique usernames or emails.
        except IntegrityError:
            return message('A user already exists with that username or email.', False)
