from unittest import TestCase
from app import app 
from models import db, Pet


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class PetModelTestCase(TestCase):
    
    # ----------Set up--------------------------------
    def setUp(self):
        Pet.query.delete()
        pet = Pet(name="Jinja", species="cat")
        db.session.add(pet)
        db.session.commit()
        self.id = pet.id
        
    def tearDown(self):
        db.session.rollback()

    # ----------Test Models---------------------------
    def test_add_new_pet(self):
        Pet.add_new_pet("tiger","cat")
        pets = db.session.query(Pet).count()
        self.assertEqual(2, pets)
        
    def text_get_all_pets(self):
        pets = Pet.get_all_pets()
        self.assertEqual(1, len(pets))
        
    def test_get_by_id(self):
        pet = Pet.get_by_id(self.id) 
        self.assertEqual(pet.id, self.id)   
    
    def test_get_by_name(self):
        pet1 = db.session.query(Pet).first()
        test_name = pet1.name 
        pet2 = Pet.get_by_name(test_name)
        self.assertEqual(test_name, pet2[0].name)
        
    def test_get_by_species(self):
        pet = Pet.get_by_species("cat")
        self.assertEqual("cat", pet[0].species)
        
    def test_get_by_age(self):
        pet = Pet.get_by_age(0)
        self.assertEqual(0, pet[0].age)
        
    def test_get_by_available(self):
        pet = Pet.get_by_available()
        self.assertEqual(True, pet[0].available)
        
    def test_update_pet(self):
        Pet.update_pet(self.id, "Salty", "cat")
        pet = db.session.query(Pet).first()
        self.assertEqual("Salty", pet.name)
    
    def test_delete_pet(self):
        Pet.delete_pet(self.id)
        pets = db.session.query(Pet).count()
        self.assertEqual(0, pets)