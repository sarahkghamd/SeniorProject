from tkinter import CASCADE
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from os import path



class Admin(db.Model,UserMixin):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String(150), nullable=False)
    applicants = db.relationship('Applicant')
    videos = db.relationship('InterviewVideo')
    
  
		

class Applicant(db.Model):
    __tablename__ = 'applicant'
    phone = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150),nullable=False)
    gender = db.Column(db.String(150),nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))
    video = db.relationship('InterviewVideo')
    personality = db.relationship('PersonalityAssesment')
    
   
class InterviewVideo (db.Model):
    __tablename__ = 'interviewvideo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.DateTime(timezone=True), default= func.now(),nullable=False)
    video=db.Column(db.LargeBinary)
    applicant_phone = db.Column(db.Integer, db.ForeignKey("applicant.phone"),nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"),nullable=False)
    personality = db.relationship('PersonalityAssesment')
    frames = db.relationship('InterviewFrames')
    
class PersonalityAssesment (db.Model):
    __tablename__ = 'personalityassesment'
    op= db.Column(db.Integer)
    ex= db.Column(db.Integer)
    co= db.Column(db.Integer)
    ag= db.Column(db.Integer)
    ne= db.Column(db.Integer)
    applicant_phone = db.Column(db.Integer, db.ForeignKey("applicant.phone"))
    interview_id = db.Column(db.Integer, db.ForeignKey("interviewvideo.id"), primary_key=True)
    
class InterviewFrames (db.Model):
    interview_id = db.Column(db.Integer, db.ForeignKey('interviewvideo.id'), primary_key=True) 
    frame = db.Column(db.String(150))       