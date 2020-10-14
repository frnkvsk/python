from models import Post, db
from app import app
from datetime import datetime

# Create all tables
# db.drop_all()
# db.create_all()

# If table isn't empty, empty it
# Post.query.delete()


post1 = Posts(title="First Post", content="First Post Content", created_at=datetime(2015, 6, 5, 8, 10, 10, 10), user_id=1)
post2 = Posts(title="First Post", content="First Post Content", created_at=datetime(2015, 6, 5, 8, 10, 10, 10), user_id=2)
post3 = Posts(title="First Post", content="First Post Content", created_at=datetime(2015, 6, 5, 8, 10, 10, 10), user_id=3)
post4 = Posts(title="First Post", content="First Post Content", created_at=datetime(2015, 6, 5, 8, 10, 10, 10), user_id=4)
post5 = Posts(title="First Post", content="First Post Content", created_at=datetime(2015, 6, 5, 8, 10, 10, 10), user_id=5)
post6 = Posts(title="First Post", content="First Post Content", created_at=datetime(2015, 6, 5, 8, 10, 10, 10), user_id=6)
post7 = Posts(title="Second Post", content="Second Post Content", created_at=datetime(2015, 6, 5, 8, 10, 10, 10), user_id=1)
post8 = Posts(title="Second Post", content="Second Post Content", created_at=datetime(2015, 6, 5, 8, 10, 10, 10), user_id=2)
post9 = Posts(title="Second Post", content="Second Post Content", created_at=datetime(2015, 6, 5, 8, 10, 10, 10), user_id=3)
post10 = Posts(title="Second Post", content="Second Post Content", created_at=datetime(2015, 6, 5, 8, 10, 1, 10), user_id=4)
post11 = Posts(title="Second Post", content="Second Post Content", created_at=datetime(2015, 6, 5, 8, 10, 1, 10), user_id=5)
post12 = Posts(title="Second Post", content="Second Post Content", created_at=datetime(2015, 6, 5, 8, 10, 1, 10), user_id=6)
post13 = Posts(title="Third Post", content="Third Post Content", created_at=datetime(2015, 6, 5, 8, 10, 10, 10), user_id=1)
post14 = Post(title="Third Post", content="Third Post Content", created_at=datetime(2015, 6, 5, 8, 10, 1, 10), user_id=2)
post15 = Post(title="Third Post", content="Third Post Content", created_at=datetime(2015, 6, 5, 8, 10, 1, 10), user_id=3)
post16 = Post(title="Third Post", content="Third Post Content", created_at=datetime(2015, 6, 5, 8, 10, 1, 10), user_id=4)
post15 = Post(title="Third Post", content="Third Post Content", created_at=datetime(2015, 6, 5, 8, 10, 1, 10), user_id=5)
post16 = Post(title="Third Post", content="Third Post Content", created_at=datetime(2015, 6, 5, 8, 10, 1, 10), user_id=6)

db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.add(post4)
db.session.add(post5)
db.session.add(post6)
db.session.add(post7)
db.session.add(post8)
db.session.add(post9)
db.session.add(post10)
db.session.add(post11)
db.session.add(post12)
db.session.add(post13)
db.session.add(post14)
db.session.add(post15)
db.session.add(post16)

db.session.commit()
