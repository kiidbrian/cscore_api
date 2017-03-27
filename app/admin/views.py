from flask import render_template, session, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from . import admin
from datetime import datetime
from app import db
from models import *

import os

@admin.route('/', methods=['GET'])
def index():
    return redirect(url_for('auth.login'))


@admin.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    activities = current_user.activities
    clients_count = Client.query.count()
    invites_count = Invites.query.count()
    loan_request_count = LoanRequest.query.count() 
    users_count = User.query.count()
    activities_count = len(activities)
    return render_template('dashboard.html', activities=activities, users_count=users_count, clients_count=clients_count,\
                            activities_count=activities_count, invites_count=invites_count, loan_request_count=loan_request_count)


@admin.route('/users', methods=['GET'])
@login_required
def users_management():
    users = User.query.all()

    activity = Activity(user_id=current_user.id, description="Accessed accounts management")
    db.session.add(activity)
    db.session.commit()

    return render_template('users.html', users=users)
    

@admin.route('/users', methods=['GET','POST'])
def add_user():
    if request.method == "POST":
        fullname = "{} {}".format(request.form.get('firstname'), request.form.get('surname'))
        email = request.form.get('email')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        user = User()
        user.fullname = fullname
        user.email = email
        user.password = password
        user.created_at = datetime.now()
        user.updated_at = user.created_at

        activity = Activity(user_id=current_user.id, description="Created new account for {}".format(user.fullname))
        db.session.add(activity)
        db.session.commit()

        db.session.add(user)
        db.session.commit()

        flash("New user, {0}, created successfully.".format(fullname))
        return redirect(url_for('admin.users_management'))

    return render_template('register.html')


@admin.route('/user/<user_id>/activities')
@login_required
def user_activities(user_id):
    user = User.query.get(int(user_id))

    activity = Activity(user_id=current_user.id, description='Viewed user activity logs for {}'.format(user.fullname))
    db.session.add(activity)
    db.session.commit()

    activities = user.activities
    return render_template('user-activities.html', activities=activities)


@admin.route('/clients')
@login_required
def list_clients():
    clients = Client.query.all()
    return render_template('clients.html', clients=clients)


@admin.route('/loans')
@login_required
def list_loans():
    loans = LoanRequest.query.all()
    return render_template('loans.html', loans=loans)


@admin.route('/payments')
@login_required
def list_payments():
    payments = LoanPayments.query.all()
    return render_template('repayments.html', payments=payments)


@admin.route('/invites')
@login_required
def list_invites():
    invites = Invites.query.all()
    return render_template('invites.html', invites=invites)
# @admin.route('/reset-password', methods=['POST'])
# def reset_password():
#     pass
