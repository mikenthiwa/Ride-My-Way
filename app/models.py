# models.py
import os
import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
import datetime
import psycopg2
from instance.config import config, Config
from resources.auth import data




def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = ("""
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            email VARCHAR(150) NOT NULL,
            username VARCHAR(100) NOT NULL,
            password VARCHAR(450) NOT NULL,
            is_driver BOOLEAN NULL,
            is_admin BOOLEAN NULL)
        """,

        """ CREATE TABLE rides (
                       ride_id SERIAL PRIMARY KEY,
                       user_id INTEGER NOT NULL references users(user_id) on delete cascade,
                       route VARCHAR(155) NOT NULL,
                       driver VARCHAR(150) NOT NULL,
                       time VARCHAR(150) NOT NULL,
                       request VARCHAR(200) NULL)
        """,
        """ CREATE TABLE request (
                       id SERIAL PRIMARY KEY,
                       username VARCHAR(155) NOT NULL,
                       ride_id INTEGER NOT NULL references rides(ride_id) on delete cascade,
                       pickup_point VARCHAR(150) NOT NULL,
                       accept VARCHAR(200))
        """
        )
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(os.getenv('database'))
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

#
# conn = psycopg2.connect(os.getenv('database'))
# cur = conn.cursor()



class Users(object):
    """Contains all methods for class users"""
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv('database'))
        self.cur = self.conn.cursor()

    def get_all_user(self):
        """Get all users"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT * from users")
        rows = cur.fetchall()
        output = {}
        for row in rows:
            user_email = row[0]
            output[user_email] = {'username': row[1], 'password': row[2], 'is_driver': row[3], 'is_admin': row[4]}
            conn.close()
        return output

    def add_users(self, email, username, password):
        """Creates new user"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT email from users")
        rows = cur.fetchall()
        output = []
        for row in rows:
            user_email = row[0]
            output.append(user_email)
        if email in output:
            return {"msg": "email already exist"}

        hashed_password = generate_password_hash(password=password, method='sha256')

        query = "INSERT INTO users (user_id, email, username, password, is_driver, is_admin) VALUES " \
                "('" + email + "', '" + username + "', '" + hashed_password + "', '" + '0' +"','" + '0' +"' )"
        cur.execute(query)
        conn.commit()
        conn.close()


        return {"msg": "You have been successfully added"}

    def add_driver(self, email, username, password):
        """Creates new user"""

        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        hashed_password = generate_password_hash(password=password, method='sha256')

        query = "INSERT INTO users (email, username, password, is_driver, is_admin) VALUES " \
                "('" + email + "', '" + username + "', '" + hashed_password + "', '" + '1' +"','" + '0' +"' )"
        cur.execute(query)
        conn.commit()

        return {"msg": "You have been successfully added"}

    def login(self, email, password):
        """Login registered users"""

        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()

        cur.execute("SELECT email, user_id, username, password, is_driver, is_admin from users where email='{}'".format(email))
        rows = cur.fetchone()
        if rows is None:
            return {"msg": 'invalid email'}, 401
        if not check_password_hash(rows[3], password=password):
            return {"msg": "password do not match"}, 401

        token = jwt.encode({'email': rows[0], 'user_id': rows[1], 'username': rows[2], 'is_driver': rows[4], 'is_admin': rows[5],
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=12)},
                             os.getenv('SECRET_KEY'))

        return {'token': token.decode('UTF-8')}



    def get_a_user(self, email):
        """Get a specific user"""

        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT email, username, password, is_driver, is_admin from users;")
        rows = cur.fetchall()
        output = {}
        for row in rows:
            user_email = row[0]
            output[user_email] = {'username':row[1], 'password': row[2], 'is_driver': row[3], 'is_admin': row[4]}
        if email in output:
            return {'email': email, 'username': output[email]['username'], 'is_driver': output[email]['is_driver']}


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

    def __del__(self):
        self.conn.close()


def invalid_ride_id():
    """Returns a message for invalid id"""
    return {"msg": "invalid id"}


class Rides:
    """Contains methods for class ride"""

    def __init__(self):
        pass

    def get_rides(self):
        """Gets all rides"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT ride_id, route, driver, time, request from rides")
        rows = cur.fetchall()

        output = {}
        for row in rows:
            ride_id = row[0]
            output[ride_id] = {"route": row[1], "time": row[2], "driver": row[3], "request": row[4]}

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
    def add_ride(route, time, requests="Request to join this ride"):
        """Add new ride"""
        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()


        print(data)
        query = "INSERT INTO rides (user_id, route, driver, time, request) VALUES " \
                "('" + str(data['user_id']) + "', '" + route + "', '" + time + "', '" + data['username'] + "', '" + requests + "')"

        cur.execute(query)
        conn.commit()
        return {"msg": "Ride has been successfully added"}

    def request_ride(self, ride_id, pickup_point):
        """Request a ride"""

        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        token = request.headers['x-access-token']
        data = jwt.decode(token, Config.SECRET)

        joined = "joined"
        query = "INSERT INTO request (username, ride_id, pickup_point, accept) VALUES ('" + str(data['username']) + "', '" + str(ride_id) + "', '" + pickup_point + "', '" + joined +"')"
        cur.execute(query)

        conn.close()
        return {"msg": "You have successfully requested a ride"}

    def get_all_requested_rides(self):
        """Driver can request all rides"""

        conn = psycopg2.connect(os.getenv('database'))
        cur = conn.cursor()
        cur.execute("SELECT * from request")
        rows = cur.fetchall()
        output = {}
        for row in rows:
            request_id = row[0]
            output[request_id] = {"ride_id": row[0], "username": row[1], "pickup_point": row[2], "time": row[3], "accept": row[4]}

        return output
        # print(rows)


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

        conn.close()
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
