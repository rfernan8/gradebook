from app import db

class Student(db.Model):
    __tablename__ = 'student' # specify the table name if it is different from class name
    sid = db.Column(db.Integer, primary_key=True) # define ID 
    first_name = db.Column(db.String(), nullable=False) # define description
    last_name = db.Column(db.String(), nullable=False, default=False)
    
class Teacher(db.Model):
    __tablename__ = 'teacher'
    tid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False)
    
class Parent(db.Model):
    __tablename__ = 'parent'
    pid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(), nullable=False) 
    
class Teaches(db.Model):
    __tablename__ = 'teaches'
    tid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, primary_key=True)    

class Enrolled(db.Model):
    __tablename__ = 'enrolled'
    sid = db.Column(db.Integer, primary_key=True)
    cid = db.Column(db.Integer, primary_key=True)    
    
class Assignment(db.Model):
    __tablename__ = 'enrolled'
    cid = db.Column(db.Integer, primary_key=True)
    aid = db.Column(db.Integer, primary_key=True)    
    letter = db.Column(db.String(), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    
class Class(db.Model):
    __tablename__ = 'class'
    cid = db.Column(db.Integer, primary_key=True)
    tid = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String(), nullable=False)
 
class Category(db.Model):
    __tablename__ = 'category'
    cid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), primary_key=True)    
    weight = db.Column(db.Weight, nullable=False)