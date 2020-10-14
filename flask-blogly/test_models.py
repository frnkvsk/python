from unittest import TestCase
from app import app
from models import db, User, Posts, Tag, PostTag
from datetime import datetime

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for Users."""

    def setUp(self):
        """Clean up any existing users."""
        PostTag.query.delete()
        Tag.query.delete()
        Posts.query.delete()
        User.query.delete()
        """Create a test user"""
        user = User(first_name="Jimmy", last_name="Tester", image_url="/static/default.jpg")
        db.session.add(user)
        db.session.commit()
        self.id = user.id 
        
        """Create a test post"""
        post = Posts(title="Test Title", content="Test Content", user_id=self.id)
        db.session.add(post)
        db.session.commit()
        self.post_id = post.id 
        
        """Create a test tag"""
        tag = Tag(name="TestTag")
        db.session.add(tag)
        db.session.commit()
        self.tag_id = tag.id 
        
        """Create a test post tag"""
        post_tag = PostTag(post_id=self.post_id, tag_id=self.tag_id)
        db.session.add(post_tag)
        db.session.commit()        
        
    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    # ---------- Test User ------------------------------------------
    
    def test_add_new_user(self):
        User.add_new_user("Mary","Tester", "/static/default.jpg")
        user = User.query.filter_by(first_name='Mary').first()
        self.assertEqual("Mary", user.first_name)
        
    def test_get_by_id(self):
        user1 = User.query.all()
        test_id = user1[0].id
        user = User.get_by_id(test_id)
        self.assertEqual(test_id, user.id)
    
    def test_set_user(self):
        user = User.query.limit(1).all()
        test_id = user[0].id
        User.set_user(test_id,"Mary","Tester", "/static/default.jpg")
        test_user = User.get_by_id(test_id)
        self.assertEqual("Mary", test_user.first_name)
    
    def test_delete_user(self):
        before = db.session.query(User).count()
        User.delete_user(self.id)
        after = db.session.query(User).count()
        self.assertEqual(before - 1, after)
        
   # ---------- Test Posts -----------------------------------------
      
    def test_add_new_post(self):
        before = db.session.query(Posts).count()
        Posts.add_new_post("Test Title", "Test Content", self.id)
        after = db.session.query(Posts).count()
        self.assertEqual(before + 1, after)
    
    def test_get_posts_by_user_id(self):
        before = db.session.query(Posts).count()
        user = User.query.all()
        test_id = user[0].id
        post = Posts.get_posts_by_user_id(self.id)
        after = db.session.query(Posts).count()
        self.assertEqual(test_id, post[0].user_id)
        
    def test_get_post_by_post_id(self):
        user = User.query.all()
        test_id = user[0].id
        post = Posts.get_post_by_post_id(self.post_id)
        self.assertEqual(test_id, post.user_id)
        
    def test_set_post(self):
        post1 = db.session.query(Posts).first()
        test_title = post1.title
        test_content = post1.content
        Posts.set_post(post1.id, "New Title", "New Content")
        post2 = db.session.query(Posts).filter_by(id = post1.id).first()
        self.assertEqual(post1.id, post2.id)
        self.assertNotEqual(test_title, post2.title)
        self.assertNotEqual(test_content, post2.content)
        self.assertEqual(post2.title, "New Title")
        self.assertEqual(post2.content, "New Content")

    def test_delete_post(self):
        before = db.session.query(Posts).count()
        Posts.delete_post(self.post_id)
        after = db.session.query(Posts).count()
        self.assertEqual(before - 1, after)
        
    # ---------- Test Tag -----------------------------------------
    
    def test_get_tags(self):
        tag = Tag.get_tags()
        self.assertEqual(1, len(tag))
        
    def test_get_tag_by_id(self):
        tag = Tag.get_tag_by_id(self.tag_id)            
        self.assertEqual(self.tag_id, tag.id)
    
    def test_is_name_exists(self):
        tag = db.session.query(Tag).first()
        exists = Tag.is_name_exists(tag.name)
        self.assertTrue(exists)
        
    def test_add_new_tag(self):
        before = db.session.query(Tag).count()
        Tag.add_new_tag('TestTag1')
        after = db.session.query(Tag).count()        
        self.assertEqual(before + 1, after)
        
    def test_set_tag(self):
        before = db.session.query(Tag).first()
        test_name = before.name
        Tag.set_tag(before.id, 'TestTag2')
        after = db.session.query(Tag).filter_by(id=before.id).first()
        self.assertNotEqual(test_name, after.name)
        self.assertEqual(before.id, after.id)
           
    def test_delete_tag(self):
        before = db.session.query(Tag).count()
        tag = db.session.query(Tag).first()
        test_id = tag.id
        Tag.delete_tag(test_id)
        after = db.session.query(Tag).count()
        self.assertEqual(before - 1, after)     
        
    