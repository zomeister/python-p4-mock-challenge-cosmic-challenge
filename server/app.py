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
                "id": scientist.id, # "id": 1,
                "name": scientist.name,
                "field_of_study": scientist.field_of_study,
            }
            scientists.append(scientist_dict)
        response = make_response(jsonify(scientists), 200)
        return response
    
    elif request.method == 'POST':
        try:
            new_scientist = Scientist(
                name=request.form.get('name'),
                field_of_study=request.form.get('field_of_study'),
            )
            
            db.session.add(new_scientist)
            db.session.commit()
            
            return make_response(
                new_scientist.to_dict(),
                201
            )
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)

@app.route('/scientists/<int:id>', methods = ['GET', 'PATCH', 'DELETE'])
def scientist_by_id(id):
    if request.method == 'GET':
        scientist = Scientist.query.filter(Scientist.id == id).one_or_none()
        if scientist is None:
            return make_response({'error': 'Scientist not found'}, 404)
        
        scientist_dict = {
            "name": scientist.name,
            "field_of_study": scientist.field_of_study,
            "missions": [m.to_dict() for m in scientist.missions] if scientist.missions else [],
        }
        response = make_response(jsonify(scientist_dict), 200)
        return response
    elif request.method == 'PATCH':
        scientist = Scientist.query.filter(Scientist.id == id).one_or_none()
        if scientist is None:
            return make_response({'error': 'Scientist not found'}, 404)
        fields = request.get_json()
        try:
            for field in fields:
                setattr(scientist, field, fields[field])
            db.session.add(scientist)
            db.session.commit()
            return make_response(scientist.to_dict(rules=('-planets', '-missions')), 202)
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)
        
    elif request.method == 'DELETE':
        scientist = Scientist.query.filter(Scientist.id == id).one_or_none()

        if scientist is None:
            return make_response({'error': 'Scientist not found'}, 404)
        db.session.delete(scientist)
        db.session.commit()
        response_body = {
            "delete_successful": True,
            "message": "Review deleted."    
        }
        response = make_response(
            response_body,
            204
        )
        return response
@app.route('/planets')
def planets():
    planets = []
    for p in Planet.query.all():
        p_dict = {
            "id": p.id,
            "name": p.name,
            "distance_from_earth": p.distance_from_earth,
            "nearest_star": p.nearest_star,
        }
        planets.append(p_dict)
    response = make_response(jsonify(planets), 200)
    return response
@app.route('/missions', methods = ['POST'])
def missions():
    if request.method == 'POST':
        try:
            new_mission = Mission(
                name=request.form.get('name'),
                scientist_id=request.form.get('scientist_id'),
                planet_id=request.form.get('planet_id')
            )
            
            db.session.add(new_mission)
            db.session.commit()
            
            return make_response(
                new_mission.to_dict(),
                201
            )
        except ValueError:
            return make_response({"errors": ["validation errors"]}, 400)
        
if __name__ == '__main__':
    app.run(port=5555, debug=True)
    


# FAILED ../Flask application in app.py returns a 400 status code and error message if a POST request to /scientists fails. - KeyError: 'errors'
# FAILED ../Flask application in app.py returns an error message if a PATCH request to /scientists/<int:id>  is invalid. - assert 500 == 400