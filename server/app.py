#!/usr/bin/env python3

from models import db, Scientist, Mission, Planet
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask import Flask, make_response, jsonify, request
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)


@app.route('/')
def home():
    return ''

@app.route('/scientists', methods = ['GET', 'POST'])
def scientists():
    if request.method == 'GET':
        scientists = []
        for scientist in Scientist.query.all():
            scientist_dict = {
                "name": scientist.name,
                "field_of_study": scientist.field_of_study,
            }
            scientists.append(scientist_dict)
        response = make_response(jsonify(scientists), 200)
        return response
    elif request.method == 'POST':
        new_scientist = Scientist(
            name=request.form.get('name'),
            field_of_study=request.form.get('field_of_study'),
        )
        db.session.add(new_scientist)
        db.session.commit()
        scientist_dict = new_scientist.to_dict()
        response = make_response(
            scientist_dict,
            201
        )
        return response

@app.route('/scientists/<int:id>', methods = ['GET'])
def scientist_by_id(id):
    if request.method == 'GET':
        scientist = Scientist.query.filter(Scientist.id == id).first()
        scientist_dict = {
            "name": scientist.name,
            "field_of_study": scientist.field_of_study,
        }
        response = make_response(jsonify(scientist_dict), 200)
        return response

@app.route('/planets')
def planets():
    planets = []
    for p in Planet.query.all():
        p_dict = {
            "name": p.name,
            "distance_from_earth": p.distance_from_earth,
            "nearest_star": p.nearest_star,
        }
        planets.append(p_dict)
    response = make_response(jsonify(planets), 200)
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
