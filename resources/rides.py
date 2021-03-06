from flask_restplus import Resource, Namespace, reqparse, fields
from app.models import Rides
from resources.auth import token_required

rides = Rides()

api = Namespace("Rides",  description="Passenger related operations")

request_model = api.model('Request Model', {'username': fields.String,
                                            "pickup_point": fields.String,
                                            "time": fields.String})

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
        """get a ride(passenger)"""

        response = rides.get_ride(ride_id=ride_id)
        return response

class RequestRide(Resource):
    """Contain PATCH method"""

    @api.expect(request_model)
    @api.doc(security='apikey')
    @token_required
    def post(self, ride_id):
        """Request ride"""
        parser = reqparse.RequestParser()
        parser.add_argument('pickup_point', required=True, type=str, help='Pickup_point is required', location=['json'])


        args = parser.parse_args()
        pickup_point = args['pickup_point']

        res = rides.request_ride(ride_id=ride_id, pickup_point=pickup_point)
        return res


api.add_resource(RideList, '/rides', endpoint='ridelist')
api.add_resource(Ride, '/rides/<int:ride_id>')
api.add_resource(RequestRide, '/users/rides/<int:ride_id>/request')

