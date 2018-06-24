# models.py

import jwt
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import os

from app import db


class Users(db.Model):
    """This class represents Users Table"""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    password = db.Column(db.String(128))
    is_driver = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    # def __repr__(self):
    #     return '<User %r>' % self.username

    def get_all_user(self):
        users = Users.query.all()
        output = []
        for user in users:
            user_data = {}
            user_data['id'] = user.id
            user_data['email'] = user.email
            user_data['username'] = user.username
            user_data['password'] = user.password
            user_data['is_driver'] = user.is_driver
            user_data['is_admin'] = user.is_admin

            output.append(user_data)

        return {"Users": output}

    @classmethod
    def add_users(cls, email, username, password):
        hashed_password = generate_password_hash(password=password, method='sha256')
        new_user = cls(email=email, username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return {"msg": "You have been successfully added"}

    @classmethod
    def add_driver(cls, email, username, password):
        hashed_password = generate_password_hash(password=password, method='sha256')
        new_user = cls(email=email, username=username, password=hashed_password, is_driver=True)
        db.session.add(new_user)
        db.session.commit()

        return {"msg": "You have been successfully added "}


    def login(self, email, password):

        user = Users.query.filter_by(email=email).first()
        if not user:
            return {"msg": "email is not available"}, 401

        if check_password_hash(user.password, password):
            driver = user.is_driver
            admin = user.is_admin
            token = jwt.encode({'email': user.email, 'is_driver': driver, 'is_admin': admin,
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(weeks=12)},
                               os.getenv('SECRET_KEY'))

            return {'token': token.decode('UTF-8')}


        return {"msg": "password do not match"}, 401

        # return {"msg": 'invalid email'}, 401

    def get_a_user(self, email):
        user = Users.query.filter_by(email=email).first()
        if not user:
            return {"msg": "email is not available"}, 401

        return {"user_id": user.id, "email": user.email, "password": user.password, "driver": user.is_driver}

    def delete_user(self, email):
        user = Users.query.filter_by(email=email).first()
        if not user:
            return {"msg": "email is not available"}, 401

        db.session.delete(user)
        return {"msg": 'user deleted'}

    def modify_username(self, email, username):
        user = Users.query.filter_by(email=email).first()
        if not user:
            return {"msg": "email is not available"}, 401
        user.username = username
        db.session.commit()
        return {"msg": 'username changed'}

    def promote_user(self, email):
        user = Users.query.filter_by(email=email).first()
        if not user:
            return {"msg": "email is not available"}, 401
        user.is_admin = True
        db.session.commit()
        return {"msg": 'user is admin!'}

    def reset_password(self, email, password):
        user = Users.query.filter_by(email=email).first()
        if not user:
            return {"msg": "email is not available"}, 401

        hashed_password = generate_password_hash(password=password, method='sha256')
        user.password = hashed_password
        db.session.commit()
        return {"msg": "password changed!"}


class Rides(db.Model):
    """Contains methods for class ride"""
    __tablename__ = 'rides'

    id = db.Column(db.Integer, primary_key=True)
    route = db.Column(db.String(60), unique=True)
    driver = db.Column(db.String(200), unique=True)
    time = db.Column(db.String(50))
    request = db.Column(db.Boolean, default=False)

    # def __repr__(self):
    #     return '<Ride %r>' % self.route


    @staticmethod
    def get_rides():
        rides = Rides.query.all()
        output = []
        for ride in rides:
            data = {}
            data["ride_id"] = ride.id
            data["route"] = ride.route
            data["driver"] = ride.driver
            data["time"] = ride.time
            data["request"] = ride.request
            output.append(data)
        return output

    def get_ride(self, ride_id):
        ride = Rides.query.get(ride_id)
        if not ride:
            return {"msg": "invalid ride_id"}, 404

        return {"ride_id": ride.id, "route": ride.route, "driver": ride.driver,
                "time": ride.time, "request": ride.request}

    @classmethod
    def add_ride(cls, route, driver, time):
        new_ride = cls(route=route, driver=driver, time=time)
        db.session.add(new_ride)
        db.session.commit()

        return {"msg": "Ride has been successfully added"}

    @staticmethod
    def modify_driver(ride_id, driver):
        ride = Rides.query.get(ride_id)
        if not ride:
            return {"msg": "Ride is not available"}, 404

        ride.driver = driver
        db.session.commit()

        return {"msg": "Driver has been successfully modified"}

    @staticmethod
    def modify_route(ride_id, route):
        ride = Rides.query.get(ride_id)
        if not ride:
            return {"msg": "Ride is not available"}, 404
        ride.route = route
        db.session.commit()
        return {"msg": "Route has been successfully modified"}

    @staticmethod
    def modify_time(ride_id, time):
        ride = Rides.query.get(ride_id)
        if not ride:
            return {"msg": "Ride is not available"}, 404
        ride.time = time
        db.session.commit()
        return {"msg": "Ride time has been successfully modified"}

    @staticmethod
    def delete_ride(ride_id):
        ride = Rides.query.get(ride_id)
        if not ride:
            return {"msg": "Ride is not available"}

        db.session.delete(ride)
        db.session.commit()
        return {"msg": "Ride has been successfully deleted"}


class Request(db.Model):
    """This class represents class table"""

    __tablename__ = 'requests'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True)
    pickup_point = db.Column(db.String(60), unique=True)
    time = db.Column(db.String(50))
    accept = db.Column(db.Boolean, default=False)

    # def __repr__(self):
    #     return '<User %r>' % self.username


    @classmethod
    def request_ride(cls, username, pickup_point, time):
        # request_ride = Request.query.get(id)
        # if not request_ride:
        #     return {"msg": "Ride is not available"}
        # request_ride.accept = True

        new_request = cls(username=username, pickup_point=pickup_point, time=time)
        db.session.add(new_request)
        db.session.commit()
        return {"msg": "You have successfully requested a ride"}

    def get_all_requested_rides(self):
        requests = Request.query.all()
        output = []
        for request in requests:
            data = {}
            data["ride_id"] = request.id
            data["username"] = request.username
            data["pickup_point"] = request.pickup_point
            data["time"] = request.time
            output.append(data)
        return output

    def accept_ride_taken(self, ride_id):
        ride = Rides.query.get(ride_id)
        ride.accept = True
        return {"msg": "A notification has been sent to passenger"}

