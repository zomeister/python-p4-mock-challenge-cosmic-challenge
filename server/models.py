from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.Integer)
    nearest_star = db.Column(db.String)
    
    missions = db.relationship('Mission', back_populates='planet', cascade="all, delete-orphan")
    scientists = association_proxy('missions', 'scientist', creator=lambda s: Mission(scientist=s))
    
    serialize_rules = ('-missions.planet', '-scientists.planets')
    
    def __repr__(self):
        return f"<Planet {self.name}, id: {self.id}>"


class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)
    
    missions = db.relationship('Mission', back_populates='scientist', cascade="all, delete-orphan")
    planets = association_proxy('missions', 'planet', creator=lambda p: Mission(planet=p))
    
    serialize_rules = ('-missions.scientist', '-planets.scientists')
    
    @validates('name')
    def validate_name(self, key, name):
        if not isinstance(name, str) or len(name) < 1:
            raise ValueError(f"Name must be a string with at least one character. Got {name}")
        else:
            return name
    
    @validates('field_of_study')
    def validate_field_of_study(self, key, field_of_study):
        if not field_of_study or len(field_of_study) < 1:
            raise ValueError(f"Name must be a string with at least one character. Got {field_of_study}")
        else:
            return field_of_study
        
    def __repr__(self):
        return f"<Scientist {self.name}, id: {self.id}>"


class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    scientist = db.relationship('Scientist', back_populates='missions')
    planet = db.relationship('Planet', back_populates='missions')
    
    serialize_rules = ('-scientist.missions', '-planet.missions')
    
    @validates('name')
    def validate_name(self, key, name):
        if not isinstance(name, str) or len(name) < 1:
            raise ValueError(f"Name must be a string with at least one character. Got {name}")
        else:
            return name
        
    @validates('planet_id')
    def validate_planet_id(self, key, planet_id):
        if planet_id is not None:
            return planet_id
        raise ValueError('Mission must have planet ID.')
        # if not isinstance(planet_id, int):
        #     raise ValueError(f"Planet ID must be an integer. Got {planet_id}")
        # elif planet_id < 0:
        #     raise ValueError(f"Planet ID must be a positive integer. Got {planet_id}")
        # elif not Planet.query.get(planet_id):
        #     raise ValueError(f"Planet ID must be a valid ID. Got {planet_id}")
        # else:
        #     return planet_id
        
    @validates('scientist_id')
    def validates_scientist_id(self, key, scientist_id):
        if scientist_id is not None:
            return scientist_id
        raise ValueError('Mission must have scientist ID.')
        # if not isinstance(scientist_id, int):
        #     raise ValueError(f"Planet ID must be an integer. Got {scientist_id}")
        # elif scientist_id < 0:
        #     raise ValueError(f"Planet ID must be a positive integer. Got {scientist_id}")
        # elif not Planet.query.get(scientist_id):
        #     raise ValueError(f"Planet ID must be a valid ID. Got {scientist_id}")
        # else:
        #     return scientist_id
        
    def __repr__(self):
        return f"<Mission {self.name}, id: {self.id}>"
