from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.objects(username=user_id).first()

class Profile(db.Document):
    job_title = db.StringField(max_length=100)
    company = db.StringField(max_length=100)
    bio = db.StringField(max_length=500)
    location = db.StringField(max_length=100)
    linkedin = db.URLField()
    github = db.URLField()

class User(db.Document, UserMixin):
    username = db.StringField(required=True, unique=True, min_length=1, max_length=40)
    email = db.EmailField(required=True, unique=True)
    password = db.StringField(required=True)
    profile_pic = db.ImageField()
    profile = db.ReferenceField(Profile, null=True)

    # Returns unique string identifying our object
    def get_id(self):
        return self.username

class Quiz(db.Document):
    respondent = db.ReferenceField(User, required=True)
    