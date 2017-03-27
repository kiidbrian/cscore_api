from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from . import auth
from models import User, Activity
from datetime import datetime
from app import db


@auth.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


@auth.route('/authenticate', methods=['POST'])
def authenticate():
    user = User.query.filter_by(email=request.form.get('email')).first()
    if user is not None and user.verify_password(request.form.get('password')):
        login_user(user)
        user.last_login_at = datetime.now()

        activity = Activity(description='Logged into system', user_id=user.id)

        db.session.add(user)
        db.session.add(activity)
        db.session.commit()
        
        return redirect(url_for('admin.dashboard'))
    flash('Invalid username or password')
    return redirect(url_for('auth.login'))


@auth.route('/logout', methods=['GET'])
def logout():
    activity = Activity(description='Logged out of system', user_id=current_user.id)
    db.session.add(activity)
    db.session.commit()
    
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('admin.dashboard'))


@auth.route('/recoverpw', methods=['GET','POST'])
def recover_password():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form.get('username')).first()
        if user is not None:
            # TODO: Implement feature
            activity = Activity(description='Request to recovery password', user_id=user.id)
    
    return render_template('recoverpw.html')


@auth.route('/users', methods=['GET', 'POST'])
def register_user():
    if request.method == "POST":
        fullname = "{} {}".format(request.form.get('firstname'), request.form.get('lastname'))
        email = request.form.get('email')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        user = User()
        user.fullname = fullname
        user.email = email
        user.password = password
        user.created_at = datetime.now()
        user.updated_at = user.created_at

        db.session.add(user)
        db.session.commit()

        flash("New user, {0}, created successfully.".format(fullname))
        return redirect(url_for('auth.register_user'))
    
    return render_template('register.html')
