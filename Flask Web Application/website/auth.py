from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Admin, Applicant, InterviewVideo
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .views import *
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        id = request.form.get('id')
        passsword = request.form.get('password')

        admin = Admin.query.filter_by(id=id).first()
        print(admin)
        if admin==None:
              flash('ID does not exist.', category='error')
        else:
            if check_password_hash(admin.password,passsword):
                flash('Logged in successfully!', category='success')
                login_user(admin, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        admin = Admin.query.filter_by(id=id).first()
        if admin:
            flash('ID already exists.', category='error')
        elif len(name) < 2:
            flash('name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_admin = Admin(id=id, name=name, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_admin)
            db.session.commit()
            login_user(new_admin, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/add-applicant', methods=['GET','POST'])
def add_applicant():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        age = request.form.get('age')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        applicant = Applicant.query.filter_by(phone=phone).first()
        emailcheck=Applicant.query.filter_by(email=email).first()
        if applicant:
            flash('Phone number already exists.', category='error')
        elif emailcheck:
            flash('Email already exists.', category='error')    
        elif len(name) < 2:
            flash('name must be greater than 1 character.', category='error')
        elif len(phone) != 10:
            flash('phone must be 10 digits.', category='error')    
        else:
            new_applicant = Applicant(phone=phone, name=name, email=email, age=age,gender=gender)
            db.session.add(new_applicant)
            db.session.commit()
            flash('Applicant added!', category='success')
            return redirect(url_for('auth.add_applicant'))
    return render_template("add_applicant.html",data=[{'name':'male'}, {'name':'female'}], user=current_user)

@auth.route('/upload-interview', methods=['GET','POST'])
def upload_interview():
    if request.method == 'POST':
        file = request.files['file'] 
        nname= request.form.get('applicant')
 
        result = Applicant.query.filter_by(name=nname).first()
        
        new_interview = InterviewVideo(video=b'file', applicant_phone=result.phone, admin_id=current_user.id )
        db.session.add(new_interview)
        db.session.commit()
        videoToframes(file)
    return render_template("upload_interview.html", user=current_user,query=Applicant.query.all())

@auth.route('/view-reports', methods=['GET','POST'])
def viewR():
    return render_template("viewR.html", user=current_user)

@auth.route('/view-applicants', methods=['GET','POST'])
def viewA():
    
        
    return render_template("viewA.html", user=current_user,query=Applicant.query.all())

@auth.route('/applicant-report', methods=['GET','POST'])
def report():
    return render_template("report.html", user=current_user)