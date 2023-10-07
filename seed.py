from app import app
from config import db

from models import User, Wedding, Guest

def seedData():
    print("deleting old data")
    # User.query.delete()
    # Wedding.query.delete()
    db.create_all()
    print("seeding new data")

# using an unencrypted password hash just for testing purposes
    # u1 = User(email="grace@gmail.com", first_name="grace", last_name="nieboer", _password_hash="dsgahk3w980!klf", )
    # w1 = Wedding(date="November, 2024", user_id=1)
    g1 = Guest(first_name="Johanna", last_name="Nieboer", wedding_id=1)
    g2 = Guest(first_name="Matthew", last_name="Nieboer", wedding_id=1)
    g3 = Guest(first_name="Jack", last_name="Nieboer", wedding_id=1)
    db.session.add_all([g1, g2, g3])
    db.session.commit()

    print("Seeding complete")

if __name__ == '__main__':
    with app.app_context():
        print("Starting seed...")
        seedData()