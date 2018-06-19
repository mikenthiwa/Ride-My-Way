from flask_restplus import Resource, Namespace
from app.models import Users
from resources.auth import admin_required

user = Users()

api = Namespace('Admin', description='Admin related operation')

class Admin(Resource):
    """Contains get method"""

    @admin_required
    def get(self):
        res = user.get_all_user()
        return res

api.add_resource(Admin, '/admin/users', endpoint='admin')
