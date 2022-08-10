from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/person-outline-icon-png-person-outline-icon-png-person-17.png"


"""Models for Blogly."""
class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Blog post."""

    __tablename__ = "posts"
        
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime, 
        nullable=False, 
        default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)

    @property
    def formatted_date(self):
        '''Return foramtted date.'''
    
        return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")

class PostTag(db.Model):
    """Tag a post."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
    '''Tag that can be added to posts.'''

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship("Post", secondary="posts_tags", backref="tags")

def connect_db(app):
    """Connect database to Flask App."""
    db.app = app
    db.init_app(app)