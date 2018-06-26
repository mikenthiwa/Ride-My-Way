# models.py

import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os
import psycopg2
from instance.config import config


rides = {}
users = {}
request = {}

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = ("""
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            email VARCHAR(50) NOT NULL,
            username VARCHAR(100) NOT NULL,
            password VARCHAR(50) NOT NULL,
            is_driver BOOLEAN NULL,
            is_admin BOOLEAN NULL )
        """,

        """ CREATE TABLE rides (
                       ride_id SERIAL PRIMARY KEY,
                       route VARCHAR(155) NOT NULL,
                       driver VARCHAR(150) NOT NULL,
                       request BOOLEAN NULL)
        """,
        """ CREATE TABLE request (
                       id SERIAL PRIMARY KEY,
                       username VARCHAR(155) NOT NULL,
                       pickup_point VARCHAR(150) NOT NULL,
                       time VARCHAR(10) NOT NULL,
                       request BOOLEAN NULL)
        """
        )
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def invalid_email():
    return {"msg": "Email is not available"}


class Users:
    """Contains all methods for class users"""

    def get_all_user(self):
        return users

    def add_users(self, email, username, password, driver=False, admin=False):
        """Creates new user"""
        hashed_password = generate_password_hash(password=password, method='sha256')
        users[email] = {"username": username,
                        "password": hashed_password,
                        "is_driver": driver,
                        "is_admin": admin}
        return {"msg": "You have been successfully added"}

    def login(self, email, password):
        """Login registered users"""
        if email in users:
            if check_password_hash(users[email]['password'], password):

                user_email = email
                driver = users[email]['is_driver']
                admin = users[email]['is_admin']
                token = jwt.encode({'email': user_email, 'is_driver': driver, 'is_admin': admin,
                                    'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=12)},
                                   os.getenv('SECRET_KEY'))

                return {'token': token.decode('UTF-8')}

            else:
                return {"msg": "password do not match"}, 401
        else:
            return {"msg": 'invalid email'}, 401

    def get_a_user(self, email):
        """Get a specific user"""
        if email not in users:
            return invalid_email()
        response = users.get(email)
        return response

    def delete_user(self, email):
        "Delete a user"
        if email not in users:
            return invalid_email()
        del users[email]
        return {"msg": 'user deleted'}

    def modify_username(self, email, username):
        """Modify the username of a specific user"""
        if email not in users:
            return invalid_email()
        user = users.get(email)
        user['username'] = username
        return {"msg": 'username changed'}

    def promote_user(self, email):
        """Make a user an admin"""
        if email not in users:
            return invalid_email()
        user = users.get(email)
        user['is_admin'] = True
        return {"msg": 'user is admin!'}

    def reset_password(self, email, password):
        """Reset the password of specific user"""
        if email not in users:
            return invalid_email()
        user = users.get(email)
        hashed_password = generate_password_hash(password=password, method='sha256')
        user['password'] = hashed_password
        return {"msg": "password changed!"}


def invalid_ride_id():
    """Returns a message for invalid id"""
    return {"msg": "invalid ride_id"}


class Rides:
    """Contains methods for class ride"""

    @staticmethod
    def get_rides():
        """Gets all rides"""
        output = []
        for ride_id in rides:
            data = {}
            data["ride_id"] = ride_id
            data["route"] = rides[ride_id]["Route"]
            data["driver"] = rides[ride_id]["Driver"]
            data["time"] = rides[ride_id]["Time"]
            data["request"] = rides[ride_id]["request"]
            output.append(data)
        return output

    def get_ride(self, ride_id):
        """Get a specific ride"""
        if ride_id not in rides:
            return invalid_ride_id()

        ride = rides[ride_id]
        return ride

    @staticmethod
    def add_ride(route, driver, time, request="Request to join this ride"):
        """Add new ride"""
        new_id = len(rides) + 1
        rides[new_id] = {"Route": route,
                         "Driver": driver,
                         "Time": time,
                         "request": request}
        return {"msg": "Ride has been successfully added"}

    def request_ride(self, ride_id, username, pickup_point, time, accept="accept", reject="reject"):
        """Request a ride"""
        ride = rides.get(ride_id)
        ride["request"] = "You have requested to join this ride"
        request[ride_id] = {"route": rides[ride_id]["Route"],
                            "username": username,
                            "pickup_point": pickup_point,
                            "time": time,
                            "accept": accept,
                            "reject": reject}
        return {"msg": "You have successfully requested a ride"}

    def get_all_requested_rides(self):
        """Driver can request all rides"""
        output = []
        for ride_id in request:
            data = {}
            data["route"] = request[ride_id]["route"]
            data["username"] = request[ride_id]["username"]
            data["pickup_point"] = request[ride_id]["pickup_point"]
            data["time"] = request[ride_id]["time"]
            output.append(data)
        return output


    def accept_ride_taken(self, ride_id):
        """Driver can accept a ride selected"""
        ride = rides.get(ride_id)
        ride["accept"] = True
        return {"msg": "You have confirmed ride taken"}


    @staticmethod
    def modify_driver(ride_id, driver):
        """Changes details of a driver"""
        ride_details = rides[ride_id]
        ride_details["Driver"] = driver
        return {"msg": "Driver has been successfully modified"}

    @staticmethod
    def modify_route(ride_id, route):
        """Changes details of a route"""
        ride_details = rides[ride_id]
        ride_details["Route"] = route
        return {"msg": "Route has been successfully modified"}

    @staticmethod
    def modify_time(ride_id, time):
        """Changes time of a particular ride"""
        ride_details = rides[ride_id]
        ride_details["Time"] = time
        return {"msg": "Ride time has been successfully modified"}

    @staticmethod
    def delete_ride(ride_id):
        """Deleting a particular ride"""
        if ride_id not in rides:
            return invalid_ride_id()

        del rides[ride_id]
        return {"msg": "Ride has been successfully deleted"}
