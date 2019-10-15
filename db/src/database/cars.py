from database.db import db, conn
from database import auth, users
from MySQLdb._exceptions import IntegrityError



def add_car(user_id: int, make: str, model: str, year: int, mileage: int):
    """
    Insert a car row into the cars table.
    """
    message = lambda m, s=False: { 'message': m, 'success': s }
    query = """
        INSERT INTO `cars` (
            `user_id`,  `make`, `model`, `year`, `mileage`
        ) VALUES (%s, %s, %s, %s, %s);
    """

    user = users.get_by_id(user_id)
    if not user:
        return message('USER_NOT_FOUND')

    try:
        db.execute(query, (
            user_id, make, model, year, mileage
        ))
        conn.commit()
        return message('Car added!', True)

    except IntegrityError:
        return message('Something went wrong while adding your car.', False)


def get_cars(user_id: int):
    """
    Get a list of user's cars by the user's token.
    """
    query = """
        SELECT cars.* FROM `users`
        INNER JOIN `cars` ON users.id=cars.user_id
        WHERE users.id=%s
    """
    db.execute(query, (user_id,))
    return db.fetchall()


def get_car(user_id: int, car_id: int):
    """
    Get a car from the cars table by its id field.
    """
    query = """
        SELECT cars.* FROM `users`
        INNER JOIN `cars` ON users.id=cars.user_id
        WHERE users.id=%s AND cars.id=%s
    """
    db.execute(query, (user_id, car_id))
    return db.fetchone()


def delete_car(user_id: int, car_id: int):
    """
    Delete a car row from the cars table by its id field.
    """
    query = """
        DELETE cars.* FROM `cars`
        INNER JOIN `users` ON users.id=cars.user_id
        WHERE users.id=%s AND cars.id=%s
    """
    print(user_id, car_id)
    db.execute(query, (user_id, car_id))
