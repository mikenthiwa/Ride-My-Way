from flask_restplus import Resource, Namespace
from app.models import Rides
from resources.auth import token_required

rides = Rides()

api = Namespace("Rides",  description="Passenger related operations")


class RideList(Resource):
    """Contain GET methods"""

    @api.doc(security='apikey')
    @token_required
    def get(self):

        """Get all rides endpoint"""
        response = rides.get_rides()
        return response

class Ride(Resource):
    """Contains GET method"""

    @api.doc(security='apikey')
    @token_required
    def get(self, ride_id):
        """Passenger a ride"""

        response = rides.get_ride(ride_id=ride_id)
        return response

class RequestRide(Resource):
    """Contain PATCH method"""

    @api.doc(security='apikey')
    @token_required
    def patch(self, ride_id):
        """Post a ride"""

        res = rides.request_ride(ride_id=ride_id)
        return res


api.add_resource(RideList, '/rides', endpoint='ridelist')
api.add_resource(Ride, '/rides/<int:ride_id>')
api.add_resource(RequestRide, '/users/rides/<int:ride_id>/request')

