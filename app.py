from config import app, api, db
from flask_restful import Resource
from flask import make_response, request
from models import Wedding, User, Guest, ToDo
from datetime import datetime, timedelta
import json
import os
import jwt



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
        return make_response(user.to_dict(rules=('wedding','todos', 'guests')), 200)


####### SignIn########
class Login(Resource):
    def post(self):
        useremail = request.get_json()['email']
        password = request.get_json()['password']

        user = User.query.filter(User.email == useremail).first()

        if not user:
            print("no user found")
            return make_response({"error":"No user found"}, 401)
        
        if user.authenticate(password):
            token = jwt.encode({'id': user.id},  os.getenv('SECRET_KEY'))
            return make_response({'token': token.decode('UTF-8'), 'user':user.to_dict(rules=('wedding',))}, 200)

        return make_response({"error":"Authentication failed"}, 400)
    # expire this after 2 hours

class SignOut(Resource):
    def delete(self):
        pass
# do we even need this? on the front end we can just delete the token and it'll kick the user right out. 


class Weddings(Resource):
    def get(self):
        weddings = [w.to_dict() for w in Wedding.query.all() ]

        if len(weddings) == 0:
            return make_response({"error":"No weddings found"}, 400)

        return make_response(weddings, 200)

    def post(self):
        user_id = request.get_json()['user_id']
        wedding_date_str = request.get_json()['wedding_date']

        # Convert wedding_date_str to a Python datetime object
        wedding_date = datetime.strptime(wedding_date_str, '%Y-%m-%dT%H:%M:%S.%fZ')

        # This assumes that the incoming string will be this format string: 
        # const addWedding = async () => {
        # const weddingData = {
        #     bride_name: 'Alice',
        #     groom_name: 'Bob',
        #     wedding_date: '2023-11-05T14:30:00.000Z',  // Adjust the date format as needed
        # };

        try:
            wedding = Wedding(
                wedding_date=wedding_date,
                # this might be able to come from somewhere else?
                user_id=user_id
            )
        except:
            return make_response({"error":"Validation Error"}, 400)

        try:
            db.session.add(wedding)
            db.session.commit()
            return make_response(wedding.to_dict(), 200)
        
        except:
            return make_response({"error":"Validation Error"}, 400)
class Guests(Resource):
    def get(self):

        guests = [g.to_dict() for g in Guest.query.all()]

        if len(guests) == 0:
            return make_response({"error":"guests not found"}, 404)
            
        return make_response(guests, 200)
    
    def post(self):

        data = request.get_json()

        try:
            newGuest = Guest(
                first_name=data['first_name'],
                last_name=data['last_name'],
                user_id=data['user_id'],
            )
        except:
            print("error in creating new guest record...")
            return make_response({"error":"error in creating new Guest record"}, 400)
        try:
            db.session.add(newGuest)
            db.session.commit()

            return make_response({newGuest.to_dict()}, 201)
        except:
            print("error adding new guest to the database")
            return make_response({"error committing record to the database"}, 400)

class GuestById(Resource):
    def patch(self, id):
        guest = Guest.query.filter_by(id = id).first()
        print(guest.first_name)
        if not guest:
            return make_response({"error":"guest not found"}, 404)
        
        try:
            data = request.get_json()
            print(data)
            for key, value in data.items():
                if isinstance(value, dict):
                    # Handle nested objects
                    for nested_key, nested_value in value.items():
                        setattr(getattr(guest, key), nested_key, nested_value)
                else:
                    setattr(guest, key, value)

        except Exception as e:
            return make_response({"error": f"Error:{e}"}, 400)
        # except KeyError as e:
        #     return make_response({"error": f"KeyError: {e}"}, 400)
        # except ValueError as e:
        #     return make_response({"error": f"ValueError: {e}"}, 400)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return make_response({"error": "Validation error, unprocessable entity, check db constraint"}, 422)
    
        return make_response(guest.to_dict(), 200)

class Todos(Resource):
    def post(self):
        data = request.get_json()

        try:
            newTodo = ToDo(
                todo=data['todo'],
                isDone=False,
                user_id=data['user_id']
            )
        
        except Exception as e:
            return make_response({"error": f"Error:{e}"}, 400)
        
        try:
            db.session.add(newTodo)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return make_response({"error": "Validation error, unprocessable entity, check db constraint"}, 422)

        
api.add_resource(Home, '/')
api.add_resource(Login, '/login')
api.add_resource(Users, '/users')
api.add_resource(SignOut, '/signout')
api.add_resource(Weddings, '/weddings')
api.add_resource(UserById, '/users/<int:id>')
api.add_resource(Guests, '/guests')
api.add_resource(GuestById, '/guests/<int:id>')
api.add_resource(Todos, '/todos')


if __name__ == '__main__':
    app.run(port=5555, host='0.0.0.0', debug=True)