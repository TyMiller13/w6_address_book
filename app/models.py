from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30), nullable = False)
    email = db.Column(db.String(50), nullable = False, unique=True)
    username = db.Column(db.String(50), nullable = False, unique=True)
    password = db.Column(db.String(256), nullable = False)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs['password'])
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<User {self.id}| {self.username}>"

class address(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30), nullable = False)
    phone_number = db.Column(db.Integer(15), nullable = False, unique=True)
    address = db.Column(db.Text, nullable = False, unique=True)
    date_created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, foreign_key = True)

    def __init__(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Address {self.id}| {self.first_name} {self.last_name} {self.phone_number} {self.address}>"