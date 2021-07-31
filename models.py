from datetime import datetime

from main import db
from sqlalchemy import Sequence
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128), nullable=False)


    def __repr__(self):
        return '<Tên đầy đủ: {} {}, email: {}>'.format(self.first_name, self.last_name, self.email)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(128), nullable=False)
    category = db.Column(db.String(128), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    user_id = db.Column(db.Integer, ForeignKey('user.user_id'), nullable=False)
    user = relationship('User', backref=db.backref('posts', lazy=True))

    approve_id = db.Column(db.Integer, db.ForeignKey('approve.id'), nullable=False)
    approve = relationship('Approve', backref=db.backref('posts', lazy=True))



    def __repr__(self):
        return '<Product name: {}, category :{}, price:{},  date:{}>, user_id{}'.format(self.product_name, self.category,
                                                                                        self.price, self.date, self.user_id)

class Approve(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)

    def __repr__(self):
        return '<Approve id: {}, name :{}'.format(self.id, self.name)



db.create_all()