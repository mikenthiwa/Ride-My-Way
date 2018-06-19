# drivers.py

from flask_restplus import Resource, Namespace, reqparse, fields
from app.models import Rides

rides = Rides()

api = Namespace("Driver",  description="Driver related operations")
ride_model = api.model("Ride", {'route': fields.String,
                                'driver': fields.String,
                                'time': fields.String})

class DriverRide(Resource):
    """Contains POST method"""

    @api.expect(ride_model)
    def post(self):
        """Add a ride endpoint"""
        parser = reqparse.RequestParser()
        parser.add_argument('route', type=str, required=True, help="Route is not provided", location=['json'])
        parser.add_argument("driver", type=str, required=True, help="Driver name is not provided", location=['json'])
        parser.add_argument("time", type=str, required=True, help="Time is not provided", location=['json'])

        args = parser.parse_args()
        res = rides.add_ride(route=args['route'], driver=args['driver'], time=args['time'])
        return res, 201

class ModifyRide(Resource):
    "Contain GET PUT method"

    parser = reqparse.RequestParser()
    parser.add_argument('route', type=str, required=False, location=['json'])
    parser.add_argument("driver", type=str, required=False, location=['json'])
    parser.add_argument("time", type=str, required=False, location=['json'])

    def get(self, ride_id):

        """Get a ride """
        res = rides.get_ride(ride_id=ride_id)
        return res

    """Modifying ride detail"""

    @api.expect(ride_model)
    def put(self, ride_id):
        args = self.parser.parse_args()
        route = args['route']
        driver = args['driver']
        time = args['time']

        if route:
            res = rides.modify_route(ride_id=ride_id, route=route)
            return res

        if driver:
            res = rides.modify_driver(ride_id=ride_id, driver=driver)
            return res

        if time:
            res = rides.modify_time(ride_id=ride_id, time=time)
            return res



    def delete(self, ride_id):
        res = rides.delete_ride(ride_id=ride_id)
        return res

class AcceptRide(Resource):
    """Contain PATCH method"""

    def patch(self, ride_id):
        """Driver accepts ride taken by passenger"""

        res = rides.accept_ride_taken(ride_id=ride_id)
        return res



api.add_resource(DriverRide, '/driver/rides')
api.add_resource(ModifyRide, '/driver/rides/<int:ride_id>')
api.add_resource(AcceptRide, '/driver/rides/<int:ride_id>/accept')
