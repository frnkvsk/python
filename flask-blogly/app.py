"""Blogly application."""

from flask import Flask, request, redirect, render_template, url_for
from models import db, connect_db, User, Posts, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config["SECRET_KEY"] = "1234932718"

connect_db(app)

@app.route("/")
@app.route("/users")
def list_users():
    """List all users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("user_listing.html", users=users)

@app.route("/users/new")
def add_new_user():
    """Show new user input form"""
    return render_template("new_user_form.html")
    
@app.route("/users/new", methods=["POST"])
def do_new_user_form():
    """Handles a new user POST"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]    
    if image_url == "":
        image_url = "/static/default.jpg"        
    User.add_new_user(first_name, last_name, image_url)    
    return redirect(url_for("list_users"))

@app.route("/users/<userid>/edit")
def get_user_edit_by_id(userid):
    """Show edit user input form"""
    user = User.get_by_id(userid)
    return render_template("edit_user.html", user=user)

@app.route("/users/<userid>/edit", methods=["POST"])
def do_user_edit_by_id(userid):
    """Updates a user record""" 
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]  
    if image_url == "":
        image_url = "/static/default.jpg"
    User.set_user(userid, first_name, last_name, image_url)
    return redirect(url_for("list_users"))

@app.route("/users/<int:userid>/delete", methods=["POST"])
def do_user_delete_by_id(userid):
    """Deletes a user record"""
    User.delete_user(userid)
    return redirect(url_for("list_users"))

# ----------- POSTS ---------------------
@app.route("/users/<int:userid>")
def do_user_detail(userid):
    """Show details of a user with list of posts"""
    user = User.get_by_id(userid)
    posts = Posts.get_posts_by_user_id(userid)
    return render_template("user_detail.html", user=user, posts=posts)

@app.route("/users/<int:userid>/home_page")
def do_user_home_page(userid):
    """Show user homepage"""
    user = User.get_by_id(userid)
    posts = Posts.get_posts_by_user_id(userid)
    return render_template("home.html", user=user, posts=posts)

@app.route("/posts/<int:postid>")
def do_post_details(postid):
    """Show a post. Show buttons to edit and delete the post."""
    post = Posts.get_post_by_post_id(postid)
    user = User.get_by_id(post.user_id)
    return render_template("post_detail.html", user=user, post=post)

@app.route("/users/<int:userid>/posts/new")
def do_new_post_form(userid):
    """Add Post. Show new post input form"""
    user = User.get_by_id(userid)
    tags = Tag.get_tags()
    return render_template("new_post_form.html", user=user, tags=tags)

@app.route("/posts/<int:postid>/edit")
def do_edit_post_form(postid):
    """Show form to edit a post, and to cancel (back to user page)"""
    post = Posts.get_post_by_post_id(postid)
    user = User.get_by_id(post.user_id)
    tags = Tag.get_tags()
    return render_template("edit_post.html", post=post, user=user, tags=tags)

@app.route("/users/<int:userid>/posts/new", methods=["POST"])
def do_new_post(userid):    
    """Handle new_post_form; add post and redirect to the user detail page."""
    title = request.form["title"]
    content = request.form["content"]
    tags = request.form.getlist("tags")
    post_id = Posts.add_new_post(title, content, userid)
    PostTag.add_post_tags(post_id, tags)
    return redirect(url_for("list_users"))     
    
@app.route("/posts/<int:postid>/edit", methods=["POST"])
def do_edit_post(postid):
    """Handle editing of a post. Redirect back to the post view."""
    title = request.form["title"]
    content = request.form["content"]
    tags = request.form.getlist("tags")
    post_id = Posts.set_post(postid, title, content)       
    PostTag.add_post_tags(post_id, tags)    
    return redirect(url_for("do_post_details",postid=postid))     

@app.route("/posts/<int:postid>/delete", methods=["POST"])
def do_delete_post(postid):
    """Delete the post."""
    Posts.delete_post(postid)
    return redirect(url_for("list_users"))

# ----------- TAG ---------------------

@app.route("/tags")
def list_all_tags():
    """Lists all tags, with links to the tag detail page."""
    tags = Tag.get_tags()
    return render_template("tag_listing.html", tags=tags)

@app.route("/tags/<tagid>")
def do_show_tag(tagid):
    """Show detail about a tag. Have links to edit form and to delete."""
    tag = Tag.get_tag_by_id(tagid)
    return render_template("tag_detail.html", tag=tag)

@app.route("/tags/new")
def do_new_tag_form():
    """Shows a form to add a new tag."""
    return render_template("new_tag_form.html")

@app.route("/tags/new", methods=["POST"])
def do_new_tag():
    """Process add form, adds tag, and redirect to tag list."""
    name = request.form["name"]
    Tag.add_new_tag(name)
    return redirect(url_for("list_all_tags"))

@app.route("/tags/<tagid>/edit")
def do_edit_tag_form(tagid):
    """Show edit form for a tag."""
    tag = Tag.get_tag_by_id(tagid)
    return render_template("edit_tag.html", tag=tag)

@app.route("/tags/<tagid>/edit", methods=["POST"])
def do_edit_tag(tagid):
    name = request.form["name"]
    Tag.set_tag(tagid, name)
    return redirect(url_for("list_all_tags"))
    """Process edit form, edit tag, and redirects to the tags list."""

@app.route("/tags/<tagid>/delete", methods=["POST"])
def do_delete_tag(tagid):
    """Delete a tag."""
    tag_id = request.form["tag_id"]
    Tag.delete_tag(tag_id)
    return redirect(url_for("list_all_tags"))