
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
 
db = SQLAlchemy()


class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    

class Module(db.Model):
    __tablename__ = 'modules'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('modules.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    children = db.relationship('Module', 
                             backref=db.backref('parent', remote_side=[id]),
                             lazy='dynamic')
    

    test_cases = db.relationship('TestCase', backref='module', lazy=True,cascade='all, delete-orphan')

class TestCase(db.Model):
    __tablename__ = 'test_cases'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    module_id = db.Column(db.Integer, db.ForeignKey('modules.id',ondelete='CASCADE'), nullable=False)
    
    filename = db.Column(db.String(255)) 
    data = db.Column(db.LargeBinary)