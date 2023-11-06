from config import app, api, db
from flask_restful import Resource
from flask import make_response, request
from models import Wedding, User, Guest
import jwt
from datetime import datetime, timedelta
import json
import os




class Home(Resource):
    def get(self):
        return make_response("HOWDY")


class Users(Resource):
#    ###### SIGN UP #########
    def post(self):
        data = request.get_json()
        useremail = request.get_json()['email']
        checkuser = User.query.filter(User.email == useremail).first()
        
        if checkuser:
            return make_response({"error":"This email is already associated with an account"}, 400)
        
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

                token = jwt.encode({
                    'id': tryuser.id, 
                    # 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes = 30)
                    }, os.getenv('SECRET_KEY'))
                return make_response({'token': token.decode('UTF-8'), 'user': tryuser.to_dict()}, 201)
            
            except:
                return make_response({"error":"Validation error: unable to complete request"}, 400)

    def get(self):
        users = [user.to_dict() for user in User.query.all()]
        return make_response(users, 200)

class UserById(Resource):
    def get(self, id):
        user = User.query.filter_by(id=id).first()

        if not user:
            return make_response({"error":"no user found"}, 404)
        return make_response(user.to_dict(rules=('weddings','todos')), 200)


####### SignIn########
class Login(Resource):
    def post(self):
        useremail = request.get_json()['email']
        password = request.get_json()['password']

        user = User.query.filter(User.email == useremail).first()

        if not user:
            return make_response({"error":"No user found"}, 401)
        
        if user.authenticate(password):
            token = jwt.encode({'id': user.id},  os.getenv('SECRET_KEY'))
            return make_response({'token': token, 'user':user.to_dict()}, 200)

        return make_response({"error":"Authentication failed"}, 400)
    # expire this after 2 hours

class SignOut(Resource):
    def delete(self):
        pass
# do we even need this? on the front end we can just delete the token and it'll kick the user right out. 


class Weddings(Resource):
    def get(self):
        weddings = [w.to_dict() for w in Wedding.query.find_all() ]

        if len(weddings) == 0:
            return make_response({"error":"No weddings found"}, 400)

        return make_response(weddings, 200)

    def post(self):
        data = request.get_json()

        try:
            wedding = Wedding(
                wedding_date=data['wedding_date'],
                # this might be able to come from somewhere else?
                user_id=data['user_id']
            )
        except:
            return make_response({"error":"Validation Error"}, 400)

        try:
            db.session.add(wedding)
            db.session.commit()
            return make_response(wedding.to_dict(), 200)
        
        except:
            return make_response({"error":"Validation Error"}, 400)
        
        
api.add_resource(Home, '/')
api.add_resource(Login, '/login')
api.add_resource(Users, '/users')
api.add_resource(SignOut, '/signout')
api.add_resource(Weddings, '/weddings')
api.add_resource(UserById, '/users/<int:id>')


if __name__ == '__main__':
    app.run(port=5555, host='0.0.0.0', debug=True)