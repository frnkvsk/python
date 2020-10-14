from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, BooleanField, validators

SPECIES = ('cat', 'dog', 'porcupine')
DEFAULT_PHOTO_URL = "/static/default.jpg"
DEFAULT_NOTES = "none given"

class AddPetForm(FlaskForm):
    """Form for adding a new pet"""
    name = StringField("Pet Name", [validators.DataRequired()])
    species = SelectField("Pet Species", choices=[(species, species) for species in SPECIES])
    photo_url = StringField("Photo URL")
    age = StringField("Pet Age")
    notes = StringField("Pet Notes")
    available = BooleanField("Pet Available")
    
    def set_form(self, pet_name, pet_species, pet_photo_url, pet_age, pet_notes, pet_available):
        """Set a form with default values"""
        self.name.data = pet_name
        self.species.data = pet_species
        if pet_photo_url != DEFAULT_PHOTO_URL:
            self.photo_url.data = pet_photo_url
        self.age.data = pet_age
        if pet_notes != DEFAULT_NOTES:
            self.notes.data = pet_notes
        self.available.data = pet_available
        