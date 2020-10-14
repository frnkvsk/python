from app import app 
from models import db, Pet


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

urls = ['https://images.freeimages.com/images/thumbs/865/brunet-2-1623688.jpg',
        'https://images.freeimages.com/images/thumbs/265/dog-1249894.jpg',
        'https://images.freeimages.com/images/thumbs/b28/roscoe-1546016.jpg',
        'https://images.freeimages.com/images/large-previews/bda/bell-1401650.jpg',
        'https://i.insider.com/5df126b679d7570ad2044f3e?width=1100&format=jpeg&auto=webp',
        'https://images.freeimages.com/images/thumbs/c9b/dog-in-nature-1335831.jpg']
names = ['Coco', 'Luna', 'Sandy', 'Pete', 'Tabby', 'Lex']
species = ['dog','dog','dog','dog','cat','dog']

for x in range(6):
    pet = Pet(name=names[x], species=species[x], photo_url=urls[x], age=x)
    db.session.add(pet)
    db.session.commit()
