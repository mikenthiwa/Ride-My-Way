# models.py
import os
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import psycopg2
from instance.config import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = ("""
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            email VARCHAR(150) NOT NULL,
            username VARCHAR(100) NOT NULL,
            password VARCHAR(450) NOT NULL,
            is_driver BOOLEAN NULL,
            is_admin BOOLEAN NULL )
        """,

        """ CREATE TABLE rides (
                       ride_id SERIAL PRIMARY KEY,
                       route VARCHAR(155) NOT NULL,
                       driver VARCHAR(150) NOT NULL,
                       time VARCHAR(150) NOT NULL,
                       request VARCHAR(200) NULL)
        """,
        """ CREATE TABLE request (
                       id SERIAL PRIMARY KEY,
                       username VARCHAR(155) NOT NULL,
                       pickup_point VARCHAR(150) NOT NULL,
                       time VARCHAR(10) NOT NULL,
                       accept BOOLEAN NULL)
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
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        # connect()
        cur.execute("SELECT email, username, password, is_driver, is_admin from users")
        rows = cur.fetchall()

        output = {}
        for row in rows:
            user_email = row[0]
            output[user_email] = {'username': row[1], 'password': row[2], 'is_driver': row[3], 'is_admin': row[4]}
        return output

    def add_users(self, email, username, password):
        """Creates new user"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        hashed_password = generate_password_hash(password=password, method='sha256')

        user_email = email
        user_name = username
        user_password = hashed_password
        query = "INSERT INTO users (email, username, password, is_driver, is_admin) VALUES " \
                "('" + user_email + "', '" + user_name + "', '" + user_password + "', '" + '0' +"','" + '0' +"' )"
        cur.execute(query)

        conn.commit()
        return {"msg": "You have been successfully added"}

    def add_driver(self, email, username, password):
        """Creates new user"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        hashed_password = generate_password_hash(password=password, method='sha256')

        user_email = email
        user_name = username
        user_password = hashed_password
        query = "INSERT INTO users (email, username, password, is_driver, is_admin) VALUES " \
                "('" + user_email + "', '" + user_name + "', '" + user_password + "', '" + '1' +"','" + '0' +"' )"
        cur.execute(query)

        conn.commit()
        return {"msg": "You have been successfully added"}

    def login(self, email, password):
        """Login registered users"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT email, password, is_driver, is_admin from users")
        rows = cur.fetchall()

        output = {}
        for row in rows:
            user_email = row[0]
            output[user_email] = {'password': row[1], 'is_driver': row[2], 'is_admin': row[3]}

        if email in output:
            if check_password_hash(output[email]['password'], password=password):
                driver = output[email]['is_driver']
                admin = output[email]['is_admin']
                token = jwt.encode({'email': email, 'is_driver': driver, 'is_admin': admin,
                                    'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=12)},
                                     os.getenv('SECRET_KEY'))
                return {'token': token.decode('UTF-8')}

            else:
                return {"msg": "password do not match"}, 401
        else:
            return {"msg": 'invalid email'}, 401


    def get_a_user(self, email):
        """Get a specific user"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT email, username, password, is_driver, is_admin from users")
        rows = cur.fetchall()

        output = {}
        for row in rows:
            user_email = row[0]
            output[user_email] = {'username':row[1], 'password': row[2], 'is_driver': row[3], 'is_admin': row[4]}
        if email in output:
            return {'email': email, 'username': output[email]['username'], 'is_driver': output[email]['is_driver'] }
        return invalid_email()


    def delete_user(self, email):
        "Delete a user"
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT email, username, password, is_driver, is_admin from users")
        rows = cur.fetchall()

        output = []
        for row in rows:
            user_email = row[0]
            output.append(user_email)
        if email in output:
            cur.execute("DELETE from users where email = '" + str(email) + "'")
            conn.commit()
            return {"msg": 'user deleted'}
        else:
            return invalid_email()


    def modify_username(self, email, username):
        """Modify the username of a specific user"""

        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT email, username, password, is_driver, is_admin from users")
        rows = cur.fetchall()

        output = {}
        for row in rows:
            user_email = row[0]
            output[user_email] = {'username': row[1], 'password': row[2], 'is_driver': row[3], 'is_admin': row[4]}
        if email not in output:
            return invalid_email()
        cur.execute("UPDATE users set username = '" + username + "' where email = '" + email + "'")
        conn.commit()
        return {"msg": 'username changed'}

    def promote_user(self, email):
        """Make a user an admin"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT email, username, password, is_driver, is_admin from users")
        rows = cur.fetchall()

        output = {}
        for row in rows:
            user_email = row[0]
            output[user_email] = {'username': row[1], 'password': row[2], 'is_driver': row[3], 'is_admin': row[4]}
        if email not in output:
            return invalid_email()
        cur.execute("UPDATE users set is_admin = '" + '1' + "' where email = '" + email + "'")
        conn.commit()
        return {"msg": 'user is admin!'}

    def reset_password(self, email, password):
        """Reset the password of specific user"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT email, username, password, is_driver, is_admin from users")
        rows = cur.fetchall()

        output = {}
        for row in rows:
            user_email = row[0]
            output[user_email] = {'username': row[1], 'password': row[2], 'is_driver': row[3], 'is_admin': row[4]}
        if email not in output:
            return invalid_email()
        cur.execute("UPDATE users set password = '" + password + "' where email = '" + email + "'")
        conn.commit()
        return {"msg": "password changed!"}


def invalid_ride_id():
    """Returns a message for invalid id"""
    return {"msg": "invalid id"}


class Rides:
    """Contains methods for class ride"""

    @staticmethod
    def get_rides():
        """Gets all rides"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT ride_id, route, driver, time, request from rides")
        rows = cur.fetchall()

        output = {}
        for row in rows:
            ride_id = row[0]
            output[ride_id] = {"route": row[1], "driver": row[2], "time": row[3], "request": row[4]}

        return output

    def get_ride(self, ride_id):
        """Get a specific ride"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT ride_id, route, driver, time, request from rides")
        rows = cur.fetchall()

        output = {}
        for row in rows:
            id = row[0]
            output[id] = {"route": row[1], "driver": row[2], "time": row[3], "request": row[4]}
        if ride_id not in output:
            return invalid_ride_id(), 404

        ride = output[ride_id]
        return ride

    @staticmethod
    def add_ride(route, driver, time, request="Request to join this ride"):
        """Add new ride"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()

        query = "INSERT INTO rides (route, driver, time, request) VALUES " \
                "('" + route + "', '" + driver + "', '" + time + "', '" + request + "')"
        cur.execute(query)
        conn.commit()

        return {"msg": "Ride has been successfully added"}

    def request_ride(self, ride_id, username, pickup_point, time):
        """Request a ride"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()

        query = "INSERT INTO request (username, pickup_point, time, accept) VALUES " \
                "('" + username + "', '" + pickup_point + "', '" + time + "', '" + '0' + "')"
        cur.execute(query)
        conn.commit()
        return {"msg": "You have successfully requested a ride"}

    def get_all_requested_rides(self):
        """Driver can request all rides"""

        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT id, username, pickup_point, time, accept from request")
        rows = cur.fetchall()
        output = {}
        for row in rows:
            request_id = row[0]
            output[request_id] = {"ride_id": row[0], "username": row[1], "pickup_point": row[2], "time": row[3], "accept": row[4]}

        return output

    def accept_ride_taken(self, ride_id):
        """Driver can accept a ride selected"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT id, username, pickup_point, time from request")
        rows = cur.fetchall()
        output = {}
        for row in rows:
            request_id = row[0]
            output[request_id] = {"ride_id": row[0], "username": row[1], "pickup_point": row[2], "time": row[3]}
        if ride_id not in output:
            return invalid_ride_id()
        cur.execute("UPDATE request set accept = '" + '1' + "' where id = '" + str(ride_id) + "'")
        conn.commit()
        return {"msg": "You have confirmed ride taken"}


    @staticmethod
    def modify_driver(ride_id, driver):
        """Changes details of a driver"""

        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT ride_id, route, driver, time, request from rides")
        rows = cur.fetchall()

        output = {}
        for row in rows:
            id = row[0]
            output[id] = {"driver": row[2]}
        if ride_id not in output:
            return invalid_ride_id(), 404
        cur.execute("UPDATE rides set driver = '" + driver + "' where ride_id = '" + str(ride_id) + "'")
        conn.commit()
        return {"msg": "Driver has been successfully modified"}

    @staticmethod
    def modify_route(ride_id, route):
        """Changes details of a route"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT ride_id, route from rides")
        rows = cur.fetchall()

        output = {}
        for row in rows:
            id = row[0]

            output[id] = {"route": row[1]}

        if ride_id in output:
            cur.execute("UPDATE rides set route = '" + route + "' where ride_id = '" + str(ride_id) + "'")
            conn.commit()
            return {"msg": "Route has been successfully modified"}
        return invalid_ride_id(), 404

    @staticmethod
    def modify_time(ride_id, time):
        """Changes time of a particular ride"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT ride_id, route, driver, time, request from rides")
        rows = cur.fetchall()

        output = {}
        for row in rows:
            id = row[0]
            output[id] = {"time": row[3]}

        if ride_id not in output:
            return invalid_ride_id(), 404
        cur.execute("UPDATE rides set time = '" + time + "' where ride_id = '" + str(ride_id) + "'")
        conn.commit()
        return {"msg": "Ride time has been successfully modified"}

    @staticmethod
    def delete_ride(ride_id):
        """Deleting a particular ride"""

        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT ride_id from rides")
        rows = cur.fetchall()

        output = []
        for row in rows:
            id = row[0]
            output.append(id)


        if ride_id not in output:
            return invalid_ride_id()
        cur.execute("DELETE from rides where ride_id = '" + str(ride_id) + "'")
        conn.commit()
        return {"msg": "Ride has been successfully deleted"}
