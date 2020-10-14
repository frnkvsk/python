"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

import datetime

db = SQLAlchemy()

def connect_db(app):
    """Connect to database"""
    db.app = app
    db.init_app(app)
    
class User(db.Model):
    
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    image_url = db.Column(db.Text, nullable=False, default="/static/default.jpg")
    posts = db.relationship('Posts', backref='users', cascade="all, delete-orphan")
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @classmethod
    def add_new_user(cls, first_name, last_name, image_url):
        """Add a new user"""
        user = User(first_name=first_name, 
                    last_name=last_name, image_url=image_url)
        db.session.add(user)
        db.session.commit()
        
    @classmethod
    def get_by_id(cls, user_id):
        """Get user by user id"""
        return cls.query.filter_by(id=user_id).first()
    
    @classmethod
    def set_user(cls, user_id, first_name, last_name, image_url):
        """Update one record"""
        user = cls.query.filter_by(id=user_id).first()
        user.first_name = first_name
        user.last_name = last_name
        user.image_url = image_url
        db.session.commit()
        
    @classmethod
    def delete_user(cls, user_id):
        """Delete one record"""     
        user = cls.query.filter_by(id=user_id).first()
        db.session.delete(user)
        db.session.commit()
        
    full_name = property(get_full_name)
    

class Posts(db.Model):
    
    __tablename__ = "posts"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    posttags = db.relationship('PostTag', backref='posts', cascade="all, delete-orphan")
    @classmethod
    def add_new_post(cls, title, content, user_id):
        """Add a new post"""
        post = Posts(title=title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return post.id
        
    @classmethod
    def get_posts_by_user_id(cls, user_id):
        """Get all posts by user id"""
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def get_post_by_post_id(cls, id):
        """Get one post by post id"""
        return cls.query.filter_by(id=id).first()
    
    @classmethod
    def set_post(cls, id, title, content):
        """Update one record"""
        post = cls.query.filter_by(id=id).first()
        post.title = title
        post.content = content
        db.session.commit()
        return post.id
        
    @classmethod
    def delete_post(cls, id):
        """Delete one record"""       
        post = cls.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()
        
        
class PostTag(db.Model):
    
    __tablename__ = "post_tag"
    
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)    
   
    @classmethod
    def add_post_tags(cls, post_id, tags):
        """Add many tags to one post"""
        pt_del = db.session.query(PostTag).filter_by(post_id=post_id).all()
        for pt in pt_del:
            db.session.delete(pt)
        
        db.session.commit()
        for tag_id in tags:
            posttag = PostTag(post_id=post_id, tag_id=tag_id)
            db.session.add(posttag)
            db.session.commit()
            
class Tag(db.Model):
    
    __tablename__ = "tags"
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(25), nullable=False, unique=True)
    posttags = db.relationship('PostTag', backref='tags', cascade="all, delete-orphan")
    posts = db.relationship('Posts', secondary='post_tag', backref='tags')
    @classmethod
    def get_tags(cls):
        """Returns a List of all tags."""
        return cls.query.all()
        
    @classmethod
    def get_tag_by_id(cls, tag_id):
        """Returns a single tag based on id."""
        return cls.query.filter_by(id=tag_id).first()
    
    @classmethod
    def is_name_exists(cls, tag_name):
        return cls.query.filter_by(name=tag_name).scalar() is not None
    
    @classmethod
    def add_new_tag(cls, tag_name):
        """Creates a new tag."""
        exists = cls.is_name_exists(tag_name)
        if exists:
            return False
        else:
            tag = Tag(name=tag_name)
            db.session.add(tag)
            db.session.commit()
        
    @classmethod
    def set_tag(cls, tag_id, tag_name):
        """Updates a tag name based on id."""
        exists = cls.is_name_exists(tag_name)
        if exists:
            return False
        else:
            tag = cls.query.filter_by(id=tag_id).first()
            tag.name = tag_name
            db.session.commit()
        
    @classmethod
    def delete_tag(cls, tag_id):
        """Deletes a tag based on id."""
        tag = cls.query.filter_by(id=tag_id).first()
        db.session.delete(tag)
        db.session.commit()