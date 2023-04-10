from random import randint, choice as rc

from faker import Faker

from app import app
from models import db, Planet, Scientist, Mission

fake = Faker()

if __name__ == '__main__':

    with app.app_context():
        print("Clearing db...")
        Planet.query.delete()
        Scientist.query.delete()
        Mission.query.delete()

        print("Done seeding!")
