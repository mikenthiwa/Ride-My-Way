# users.py

from flask_restplus import Namespace, Resource, fields, reqparse
from app.models import Users

user = Users()

api = Namespace('Users', description='User related function')


class User(Resource):
    """contain PUT"""

    def put(self, email):
        """modify username"""

        parser = reqparse.RequestParser()
        parser.add_argument('username', required=False, help="No username provided", location=['json'])
        parser.add_argument('password', required=False, help="No username provided", location=['json'])

        args = parser.parse_args(strict=True)
        username = args['username']
        password = args['password']

        if username:

            res = user.modify_username(email=email, username=args['username'])
            return res

        if password:

            res =user.reset_password(email=email, password=password)
            return res

api.add_resource(User, '/auth/user/<string:email>')