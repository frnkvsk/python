from unittest import TestCase
from app import app
from models import db, User, Posts, Tag, PostTag
from datetime import datetime

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_blogly'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

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

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Users</h1>', html)
    
    def test_add_new_user(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Create a user</h1>', html)

    def test_do_new_user_form(self):
        with app.test_client() as client:
            d = {"first_name":"TestFirstName","last_name":"TestLastName", "image_url":""}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code,200)
            self.assertIn('TestFirstName',html)
            self.assertIn('TestLastName',html)
    
    def test_do_user_detail(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.id}")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code,200)
            self.assertIn('<h1>Posts</h1>',html)
            
    def test_get_user_edit_by_id(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.id}/edit")
            html = resp.get_data(as_text=True)
                   
            self.assertEqual(resp.status_code,200)
            self.assertIn('<h1>Edit a user</h1>',html)
            
    def test_do_user_edit_by_id(self):
        d = {"first_name":"TestFirstName","last_name":"TestLastName", "image_url":""}
        with app.test_client() as client:
            resp = client.post(f"/users/{self.id}/edit", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code,200)
            self.assertIn('<h1>Users</h1>', html)
            
    def test_do_user_delete_by_id(self):
        d = {"first_name":"TestFirstName","last_name":"TestLastName", "image_url":""}
        with app.test_client() as client:
            resp = client.post(f"/users/{self.id}/delete", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code,200)
            self.assertIn('<h1>Users</h1>', html)  
    
    # ----------- POSTS ---------------------
    
    def test_do_user_detail(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.id}")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code,200)
            self.assertIn('<h1>Posts</h1>', html)  
             
    def test_do_user_home_page(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.id}/home_page")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code,200)
            self.assertIn('<title>Homepage</title>', html)
                    
    def test_do_post_details(self):
        with app.test_client() as client:
            post = Posts(title="Test Title", content="Test Content", user_id=self.id)
            db.session.add(post)
            db.session.commit()
            resp = client.get(f"/posts/{post.id}")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code,200)
            self.assertIn('<title>Post Detail</title>', html)   
                   
    def test_do_new_post_form(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.id}/posts/new")  
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code,200)
            self.assertIn('<title>Add Post</title>', html)             

    def test_do_edit_post_form(self):
        with app.test_client() as client:
            post = Posts(title="Test Title", content="Test Content", user_id=self.id)
            db.session.add(post)
            db.session.commit()
            resp = client.get(f"/posts/{post.id}/edit")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code,200)
            self.assertIn('<h1>Edit Post</h1>', html) 

    def test_do_new_post(self):
        d = {"title":"Test Title","content":"Test content"}
        with app.test_client() as client:
            resp = client.post(f"/users/{self.id}/posts/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code,200)
            self.assertIn('<h1>Users</h1>', html)  
            
    def test_do_edit_post(self):   
        d = {"title":"Test1 Title","content":"Test1 content"}
        with app.test_client() as client:
            post = Posts(title="Test2 Title", content="Test2 Content", user_id=self.id)
            db.session.add(post)
            db.session.commit()
            resp = client.post(f"/posts/{post.id}/edit", data=d, follow_redirects=True) 
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code,200)
            self.assertIn('<title>Post Detail</title>', html) 
            
    def test_do_delete_post(self):
        d = {"title":"Test1 Title","content":"Test1 content"}
        with app.test_client() as client:
            post = Posts(title="Test2 Title", content="Test2 Content", user_id=self.id)
            db.session.add(post)
            db.session.commit()
            before = db.session.query(Posts).count()
            resp = client.post(f"/posts/{post.id}/delete", data=d, follow_redirects=True) 
            html = resp.get_data(as_text=True)
            after = db.session.query(Posts).count()
            
            self.assertEqual(resp.status_code,200)
            self.assertIn('<h1>Users</h1>', html) 
            self.assertEqual(before - 1, after)      
    
    # ----------- TAG ---------------------        
           
    def test_list_all_tags(self):
        with app.test_client() as client:
            resp = client.get("/tags")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code,200)
            self.assertIn('<h1>Tags</h1>', html) 
            
    def test_do_show_tag(self):
        with app.test_client() as client:
            resp = client.get(f"/tags/{self.tag_id}")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code,200)
            self.assertIn('<title>Tags</title>', html) 
            
    def test_do_new_tag_form(self):
        with app.test_client() as client:
            resp = client.get("/tags/new")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code,200)
            self.assertIn('<h1>Create a tag</h1>', html) 
            
    def test_do_new_tag(self):
        d = {"name":"New Tag"}
        with app.test_client() as client:
            before = db.session.query(Tag).count()            
            resp = client.post(f"/tags/new", data=d, follow_redirects=True) 
            html = resp.get_data(as_text=True)
            after = db.session.query(Tag).count()
            
            self.assertEqual(resp.status_code,200)
            self.assertIn('<h1>Tags</h1>', html) 
            self.assertEqual(before + 1, after)    
            
    def test_do_edit_tag_form(self):
        with app.test_client() as client:
            resp = client.get(f"/tags/{self.tag_id}/edit")
            html = resp.get_data(as_text=True)
            
            self.assertEqual(resp.status_code,200)
            self.assertIn('<h1>Edit a tag</h1>', html)
            
    def test_do_edit_tag(self):
        d = {"name":"New Tag"}
        with app.test_client() as client:
            before = db.session.query(Tag).first() 
            before_name = before.name           
            resp = client.post(f"/tags/{self.tag_id}/edit", data=d, follow_redirects=True) 
            html = resp.get_data(as_text=True)
            after = db.session.query(Tag).first()
            
            self.assertEqual(resp.status_code,200)
            self.assertIn('<h1>Tags</h1>', html) 
            self.assertNotEqual(before_name, after.name)
            
    def test_delete_tag(self):
        d = {"tag_id":f"{self.tag_id}"}
        with app.test_client() as client:
            before = db.session.query(Tag).count()
            resp = client.post(f"/tags/{self.tag_id}/delete", data=d, follow_redirects=True) 
            html = resp.get_data(as_text=True)
            after = db.session.query(Tag).count()
            
            self.assertEqual(resp.status_code,200)
            self.assertIn('<h1>Tags</h1>', html) 
            self.assertEqual(before - 1, after)        
       
            