from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

db = SQLAlchemy()
DEFAULT_PHOTO_URL = "/static/default.jpg"
DEFAULT_NOTES = "none given"

def connect_db(app):
    db.app = app
    db.init_app(app)
    
class Pet(db.Model):
    
    __tablename__ = "pets"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    species = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.Text, nullable=True, default=DEFAULT_PHOTO_URL)
    age = db.Column(db.Integer, nullable=True, default=0)
    notes = db.Column(db.Text, nullable=True, default=" ")
    available = db.Column(db.Boolean, nullable=True, default=True)
    
    # Create -------------------------------------------
    @classmethod
    def add_new_pet(cls, pet_name, pet_species, pet_photo_url=DEFAULT_PHOTO_URL, pet_age=0, pet_notes="", pet_available=True):
        if pet_photo_url == "":
            pet_photo_url = DEFAULT_PHOTO_URL
        if pet_age == "":
            pet_age = 0
        if pet_notes == "":
            pet_clnotes = DEFAULT_NOTES
        pet = Pet(name = pet_name, species = pet_species, photo_url = pet_photo_url, age = pet_age,
                  notes = pet_notes, available = pet_available)
        db.session.add(pet)
        db.session.commit()
        
    # Read ---------------------------------------------
    @classmethod
    def get_all_pets(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls, pet_id):
        return cls.query.filter_by(id=pet_id).first()
    
    @classmethod
    def get_by_name(cls, pet_name):
        return cls.query.filter_by(name=pet_name).all()
        
    @classmethod
    def get_by_species(cls, pet_species):
        return cls.query.filter_by(species=pet_species).all()
    
    @classmethod
    def get_by_age(cls, pet_age):
        return cls.query.filter_by(age=pet_age).all()
    
    @classmethod
    def get_by_available(cls):
        return cls.query.filter_by(available=True).all()
    
    # Update -------------------------------------------
    @classmethod
    def update_pet(cls, pet_id, pet_name, pet_species, pet_photo_url="", pet_age=0, pet_notes="", pet_available=True):
        pet = cls.query.filter_by(id=pet_id).first()
        pet.name = pet_name
        pet.species = pet_species
        pet.photo_url = pet_photo_url
        pet.age = pet_age
        pet.notes = pet_notes
        pet.available = pet_available
        db.session.commit()
        
    # Delete -------------------------------------------    
    @classmethod
    def delete_pet(cls, pet_id):
        pet = cls.query.filter_by(id=pet_id).first()
        db.session.delete(pet)
        db.session.commit()
    