# models.py

import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os

rides = {}
users = {}
request = {}


class Users:
    """Contains all methods for class users"""

    def get_all_user(self):
        return users

    def add_users(self, email, username, password, driver=False, admin=False):
        hashed_password = generate_password_hash(password=password, method='sha256')
        users[email] = {"username": username,
                        "password": hashed_password,
                        "is_driver": driver,
                        "is_admin": admin}
        return {"msg": "You have been successfully added"}

    def login(self, email, password):
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


def invalid_ride_id():
    return {"msg": "invalid ride_id"}

class Rides:
    """Contains methods for class ride"""

    @staticmethod
    def get_rides():
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
        if ride_id not in rides:
            return invalid_ride_id()

        ride = rides[ride_id]
        return ride

    @staticmethod
    def add_ride(route, driver, time, request="Request to join this ride", accept=False):
        new_id = len(rides) + 1
        rides[new_id] = {"Route": route,
                         "Driver": driver,
                         "Time": time,
                         "request": request,
                         "accept": accept}
        return {"msg": "Ride has been successfully added"}

    def request_ride(self, ride_id):
        ride = rides.get(ride_id)
        ride["request"] = "You have requested to join this ride"
        request[ride_id] = {"Route": rides[ride_id]["Route"]}
        return {"msg": "You have successfully requested a ride"}

    def accept_ride_taken(self, ride_id):
        ride = rides.get(ride_id)
        ride["accept"] = True
        return {"msg": "You have confirmed ride taken"}


    @staticmethod
    def modify_driver(ride_id, driver):
        ride_details = rides[ride_id]
        ride_details["Driver"] = driver
        return {"msg": "Driver has been successfully modified"}

    @staticmethod
    def modify_route(ride_id, route):
        ride_details = rides[ride_id]
        ride_details["Route"] = route
        return {"msg": "Route has been successfully modified"}

    @staticmethod
    def modify_time(ride_id, time):
        ride_details = rides[ride_id]
        ride_details["Time"] = time
        return {"msg": "Ride time has been successfully modified"}

    @staticmethod
    def delete_ride(ride_id):
        if ride_id not in rides:
            return invalid_ride_id()

        del rides[ride_id]
        return {"msg": "Ride has been successfully deleted"}
