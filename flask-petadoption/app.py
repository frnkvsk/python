from flask import Flask, request, redirect, render_template, url_for
from forms import AddPetForm
from models import db, connect_db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "1234932718"

connect_db(app)

@app.route("/")
def home():
    """Show homepage"""
    pets = Pet.get_all_pets()
    return render_template("home.html", pets=pets)

@app.route("/add", methods=["GET", "POST"])
def add_pet_form():
    """Show add pet form: handle new add"""
    form = AddPetForm()
    if form.validate_on_submit():
        Pet.add_new_pet(form.name.data, form.species.data, form.photo_url.data, 
                        form.age.data, form.notes.data, form.available.data)
        return redirect(url_for("home"))
    else:
        return render_template("pet_add_form.html", form=form)
    
@app.route("/<petid>", methods=["GET", "POST"])
def edit_pet_form(petid):
    """Show edit form"""
    form = AddPetForm()
    if form.validate_on_submit():
        Pet.update_pet(petid, form.name.data, form.species.data, form.photo_url.data, 
                       form.age.data, form.notes.data, form.available.data)
        return redirect(url_for("home"))
    else:
        pet = Pet.get_by_id(petid)
        form.set_form(pet.name, pet.species, pet.photo_url, pet.age, pet.notes, pet.available)
        return render_template("pet_edit_form.html", form=form, petid=pet.id)