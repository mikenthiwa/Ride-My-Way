from flask_restplus import Resource, Namespace
from app.models import Users
from resources.auth import admin_required

user = Users()

api = Namespace('Admin', description='Admin related operation')


class AdminUserList(Resource):
    """Contains GET method for Admin Endpoint"""

    @api.doc(security='apikey')
    # @admin_required
    def get(self):
        """get all users"""
        res = user.get_all_user()
        return res


class AdminUser(Resource):
    """Contain GET PUT PATCH"""

    @staticmethod
    @api.doc(security='apikey')
    @admin_required
    def get(email):
        """Get one users by id"""
        response = user.get_a_user(email=email)
        return response

    @api.doc(security='apikey')
    # @admin_required
    def delete(self, email):
        """Delete user"""
        response = user.delete_user(email=email)
        return response

    @api.doc(security='apikey')
    @admin_required
    def patch(self, email):
        """Update user to admin"""
        response = user.promote_user(email=email)
        return response


api.add_resource(AdminUserList, '/admin/users', endpoint='admin')
api.add_resource(AdminUser, '/admin/users/<string:email>')
