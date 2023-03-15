from email.policy import default
from xml.dom.domreg import well_known_implementations
from central import db, login
from werkzeug.security import check_password_hash, generate_password_hash
from time import time
import jwt

from flask import current_app
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(260))
    reputation = db.Column(db.Integer, default=0)
    post = db.relationship('Comment', backref='owner')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def get_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @staticmethod
    def is_unic(username, email):
        return False if User.query.filter_by(username=username, email=email).first() \
            else True

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return f'User {self.username}'
    

@login.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1000), nullable=False)
    on_article = db.Column(db.String, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))