from database.db import db
from uuid import uuid4
from hashlib import sha1



class User:
    """
    User class.
    """


    @staticmethod
    def get_by_username_or_email(username_or_email, fields='*'):
        """
        Fetch user by its username or email address.
        Returns user dict or None.
        """
        field = 'username'
        if "@" in username_or_email:
            field = 'email'

        query = "SELECT {} FROM `users` WHERE {}=%s".format(fields, field)
        db.execute(query, (username_or_email,))
        return db.fetchone()


    @staticmethod
    def get_by_token(token, fields='*'):
        """
        Fetch user by its token.
        Returns user dict or None.
        """
        query = "SELECT {} FROM `users` WHERE token=%s LIMIT 1".format(fields)
        db.execute(query, (token,))
        return db.fetchone()


    @staticmethod
    def is_token_taken(token):
        """
        Test if token is already taken.
        Returns true if token is taken.
        """
        query = "SELECT EXISTS(SELECT 1 FROM `users` WHERE token=%s) AS taken;"
        db.execute(query, (token,))
        return db.fetchone().get('taken') == 1


    @staticmethod
    def generate_token():
        """
        Generate a user token. This does not update the column.
        """
        token = None
        while not token:
            token = sha1(uuid4().urn.encode('utf-8')).hexdigest()
            if User.is_token_taken(token):
                token = None
        return token
