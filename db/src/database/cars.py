from database.db import db, conn
from database.auth import Auth
from database.user import User
from MySQLdb._exceptions import IntegrityError



class Car:

    @staticmethod
    def add_car(token: str, make: str, model: str, year: int, mileage: int):
        """
        Insert a car row into the `cars` table.
        """
        message = lambda m, s=False: { 'message': m, 'success': s }
        query = """
            INSERT INTO `cars` (
                `make`, `model`, `year`, `mileage`, `user_id`
            ) VALUES (%s,%s,%s,%s,%s);
        """

        user = User.get_by_token(token)

        if not user or not user.get('token'):
            return message('User not found.')

        try:
            db.execute(query, (
                make, model, year, mileage, user.get('id')
            ))
            conn.commit()
            return message('Car added!', True)

        except IntegrityError:
            return message('Something went wrong while adding your car.', False)


    @staticmethod
    def get_cars(token: str):
        """
        Gets a list of user's cars by the user's token.
        """
        query = """
            SELECT cars.* FROM users
            INNER JOIN cars ON users.id=cars.user_id
            WHERE users.token=%s
        """
        db.execute(query, (token,))
        return db.fetchall()


    @staticmethod
    def get_car(token: str, car_id: int):
        """
        Get a car by its id field.
        """
        query = """
            SELECT cars.* FROM `users`
            INNER JOIN `cars` ON users.id=cars.user_id
            WHERE users.token=%s AND cars.id=%s
        """
        db.execute(query, (token, car_id))
        return db.fetchone()


    @staticmethod
    def delete_car(token: str, car_id: int):
        """
        Delete a car by its id field.
        """
        query = """
            DELETE cars.* FROM `cars`
            INNER JOIN users ON users.id=cars.user_id
            WHERE users.token=%s AND cars.id=%s
        """
        db.execute(query, (token, car_id))
