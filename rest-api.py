from flask import Flask
from flask_restful import Api, Resource, reqparse


# Create the flask application and create the api object
app = Flask(__name__)
api = Api(app)

vehicles = [
    {
        "name": "redrover",
        "opcode": 1,
        "state": None
    },
    {
        "name": "cuberover",
        "opcode": 1,
        "state": None
    }
]


class Vehicle(Resource):
    def get(self, name):
        for user in vehicles:
            if name == user["name"]:
                return user, 200
        return "User not found", 404

    def post(self, name):
        """
        Will create a new user
        :param name: the same of the vehicle
        :return: a tuple with the second argument as the http status code
        """
        parser = reqparse.RequestParser()
        parser.add_argument("opcode")
        parser.add_argument("state")
        args = parser.parse_args()

        # Check if user has already been created
        for user in vehicles:
            if name == user["name"]:
                # Return 400 bad request
                return "User with name {} already exists".format(name), 400

        # Add the user to the vehicle list
        user = {
            "name": name,
            "opcode": args["opcode"],
            "state": args["state"]
        }
        vehicles.append(user)
        # Return 201, created
        return user, 201

    def put(self, name):
        """
        Will create a new user or update their info
        :param name: the name of the vehicle
        :return: tuple with the second argument as the http status code
        """
        parser = reqparse.RequestParser()
        parser.add_argument("opcode")
        parser.add_argument("state")
        args = parser.parse_args()

        # Update the user info if it is already in the list
        for user in vehicles:
            if name == user["name"]:
                user["opcode"] = args["opcode"]
                user["status"] = args["status"]
                return user, 200

        # Add the user to the vehicle list
        user = {
            "name": name,
            "opcode": args["opcode"],
            "state": args["state"]
        }
        vehicles.append(user)
        # Return 201, created
        return user, 201


    def delete(self, name):
        global vehicles
        vehicles = [user for user in vehicles if user["name"] != name]
        return "{} is deleted.".format(name), 200

api.add_resource(Vehicle, "/user/<string:name>")
app.run(debug=True)
