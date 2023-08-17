from config import app, api;
from flask_restful import Resource
from flask import make_response


class Home(Resource):
    def get(self):
        return make_response("HOWDY")


api.add_resource(Home, '/')


if __name__ == '__main__':
    app.run(port=5555, debug=True)