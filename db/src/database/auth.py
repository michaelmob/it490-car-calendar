from uuid import uuid4
from hashlib import sha1, sha256
from database.db import db, conn
from MySQLdb._exceptions import IntegrityError
from .user import User


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
        salt = sha1(encode(uuid4().urn)).hexdigest()
        password = sha256(encode(password) + encode(salt)).hexdigest()
        token = User.generate_token()

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


    @staticmethod
    def login(username_or_email, password):
        """
        Attempt to log a user in.
        Returns an API token.
        """
        user = User.get_by_username_or_email(
            username_or_email, 'password,salt,token'
        )

        # Get hashed password if user exists
        if user:
            hashed_password = sha256(
                str(password + user['salt']).encode('utf-8')).hexdigest()

        # But if user doesn't exist (we won't need the hashed_password), or the
        # users password isnt a match... deny them
        if not user or (user and user.get('password') != hashed_password):
            return { 'message': 'User does not exist.', 'success': False }

        # Return auth token
        return user.get('token')
