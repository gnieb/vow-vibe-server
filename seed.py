from app import app
from config import db

from models import User, Wedding

def seedData():
    print("deleting old data")
    User.query.delete()
    Wedding.query.delete()
    db.create_all()
    print("seeding new data")

# using an unencrypted password hash just for testing purposes
    u1 = User(email="grace@gmail.com", first_name="grace", last_name="nieboer", _password_hash="dsgahk3w980!klf", )

    db.session.add(u1)
    db.session.commit()

    print("Seeding complete")

if __name__ == '__main__':
    with app.app_context():
        print("Starting seed...")
        seedData()