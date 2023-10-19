from config import app, api, db
from flask_restful import Resource
from flask import make_response, request
from models import Wedding, User, Guest
import jwt
from datetime import datetime, timedelta
import os




class Home(Resource):
    def get(self):
        return make_response("HOWDY")


class Users(Resource):
#    ###### SIGN UP #########
    def post(self):
        data = request.get_json()
        useremail = request.get_json(['email'])
        checkuser = User.query.find_by(email=useremail).first()
        if checkuser:
            return make_response({"error":"This email is already associated mwith an account"}, 400)
        
        # otherwise, create new user.
        if checkuser == None:
            # create new user
            try:
                tryuser = User(email=useremail, first_name=data['first_name'], last_name=data['last_name'])
                password = data['password']
                tryuser.password_hash = password

            except:
                return make_response({"error":"Validation error: unable to complete request"}, 400)

            try:
                db.session.add(tryuser)
                db.session.commit()
                # JWT TOKEN SITUATION:

                token = jwt.encode({'id': tryuser.id, 'expire': datetime.utcnow() + timedelta(minutes = 60)}, os.environ['SECRET_KEY'])
                return make_response({'token': token.decode('UTF-8'), 'newuser': tryuser.to_dict()}, 201)
            
            except:
                return make_response({"error":"Validation error: unable to complete request"}, 400)

    

class UserById(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()

        if not user:
            return make_response({"error":"no user found"}, 404)
        return make_response(user.to_dict(rules=('weddings','todos')), 200)


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
api.add_resource(UserById, '/users/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, host='0.0.0.0', debug=True)