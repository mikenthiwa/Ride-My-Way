# signup_login.py

from flask_restplus import Namespace, Resource, fields, reqparse, inputs
from app.models import Users


user = Users()

api = Namespace('SignUp and Login', description='Sign-up and Login')

model_register = api.model('Sign up', {'username': fields.String(required=True),
                                       'email': fields.String(required=True),
                                       'password': fields.String(required=True),
                                       'is_driver': fields.Boolean})

# model for login
model_login = api.model('Login', {'email': fields.String,
                                  'password': fields.String})


class Register(Resource):
    """class contain POST method"""
    parser = reqparse.RequestParser()
    parser.add_argument('username', required=True, help="No username provided", location=['json'])

    parser.add_argument('email', required=True, help="No email provided", location=['json'],
                        type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"))

    parser.add_argument('password', required=True, help="No password provided", location=['json'])

    parser.add_argument('is_driver', required=False, location=['json'])

    @api.expect(model_register)
    def post(self):
        """Register user"""
        args = self.parser.parse_args(strict=True)

        username = args['username']
        email = args['email']
        password = args['password']
        driver = args['is_driver']

        if username == "" or email == "" or password == "" or driver == "":
            return {"msg": "Field cannot be empty"}

        if driver == True:
            res = user.add_driver(email=email, username=username, password=password)
            return res, 201

        driver_res = user.add_users(email=email, username=username, password=password)
        return driver_res, 201



class Login(Resource):
    """class contain post method"""
    req_data = reqparse.RequestParser()
    req_data.add_argument('email', required=True, help='username required', location=['json'],
                          type=inputs.regex(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"))

    req_data.add_argument('password', required=True, help='password required', location=['json'])

    @api.expect(model_login)
    def post(self):
        """Login user"""
        args = self.req_data.parse_args(strict=True)
        email = args['email']
        password = args['password']
        res = user.login(email=email, password=password)
        return res


api.add_resource(Register, '/register', endpoint='register')
api.add_resource(Login, '/login', endpoint='login')
