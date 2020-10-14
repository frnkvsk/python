from unittest import TestCase
from app import app
from models import db, Pet
from forms import AddPetForm

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_adopt'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        
        """Clean up any existing users."""
        Pet.query.delete()
        """Create a test user"""
        pet = Pet(name="TestPet", species="cat")
        db.session.add(pet)
        db.session.commit()
        self.id = pet.id 
        
        # self.app.config['WTF_CSRF_ENABLED'] = False
        
    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()


    def test_home(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<title>Homepage</title>', html)
    
    def test_add_pet_form(self):
        with app.test_client() as client:
            resp = client.get("/add")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<title>Add New Pet</title>', html)

    def test_add_pet_form(self):
        with app.test_client() as client:
            d = {"name":"TestFirstName","species":"cat", "photo_url":"/static/default.jpg", "age":"2", "notes":"test notes", "available":"True"}
            resp = client.post("/add", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code,200)
            self.assertIn('<title>Homepage</title>', html)
    