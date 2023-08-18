from config import app, api;
from flask_restful import Resource
from flask import make_response, request
from models import Wedding, User



class Home(Resource):
    def get(self):
        return make_response("HOWDY")


class Users(Resource):
   ###### SIGN UP #########
    def post(self):
        useremail = request.get_json(['email'])
        checkuser = User.query.find_by(email=useremail).first()
        if checkuser:
            return make_response({"error":"This email is already associated mwith an account"}, 400)
        
        # otherwise, create new user.


####### SignIn########
class SignIn(Resource):
    def post(self):
        pass
    # expire this after 2 hours

class SignOut(Resource):
    def delete(self):
        pass

class CheckSession(Resource):
    def get(self):
        pass


api.add_resource(Home, '/')
api.add_resource(SignIn, '/signin')
api.add_resource(Users, '/signup')
api.add_resource(SignOut, '/signout')
api.add_resource(CheckSession, '/checksession')


if __name__ == '__main__':
    app.run(port=5555, debug=True)