from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(50), nullable = False, unique=True)
    username = db.Column(db.String(50), nullable = False, unique=True)
    password = db.Column(db.String(256), nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    address = db.relationship('Address', backref = 'author', lazy = 'dynamic')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.id}| {self.username}>"

    def check_password(self, password_guess):
        return check_password_hash(self.password, password_guess)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class Address(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30), nullable = False)
    phone_number = db.Column(db.Integer, nullable = False, unique=True)
    address = db.Column(db.Text, nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Address {self.id}| {self.first_name} {self.last_name} {self.phone_number} {self.address}>"

    def update(self, **kwargs):
    # for each keyvalue that comes in as a keyword
        for key,value in kwargs.items():
            # if the key is an acceptable
            if key in {'first_name','last_name', 'phone_number', 'address'}:
                #set that attribute on the instance e.g. post.title = 'Updated Title'
                setattr(self,key,value)
        # save the updates to the database
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
