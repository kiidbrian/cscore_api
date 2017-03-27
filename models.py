from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import login_manager

import datetime


# BASE MODEL DEFINITION
class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp())


# USER MODEL DEFINITION
class User(BaseModel):
    __tablename__ = 'users'

    email = db.Column(db.String(255), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    fullname = db.Column(db.String(255), nullable=True)
    last_login_at = db.Column(db.DateTime, nullable=True)
    activities = db.relationship('Activity', backref='user', cascade='all, delete-orphan')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribue')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return True


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ACTIVITY MODEL DEFINITION
class Activity(BaseModel):
    __tablename__ = 'activities'

    description = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'))


class Client(BaseModel):
    __tablename__ = 'clients'

    fullname = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    weekly_income = db.Column(db.String(255), nullable=False)
    home_address = db.Column(db.String(255), nullable=True)
    work_address = db.Column(db.String(255), nullable=True)
    phone_number = db.Column(db.String(255), nullable=False)
    pin_hash = db.Column(db.String(255), nullable=False)
    occupation = db.Column(db.String(255), nullable=True)
    status = db.Column(db.String(255), nullable=True)
    last_login_at = db.Column(db.DateTime, nullable=True)
    last_logout_at = db.Column(db.DateTime, nullable=True)
    invites = db.relationship('Invites', backref='client', cascade='all, delete-orphan')
    loan_requests = db.relationship('LoanRequest', backref='client', cascade='all, delete-orphan')

    @property
    def pin(self):
        raise AttributeError('pin is not a readable attribue')

    @pin.setter
    def pin(self, pin):
        self.pin_hash = generate_password_hash(pin)

    def verify_pin(self, pin):
        return check_password_hash(self.pin_hash, pin)
    
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id


class Invites(BaseModel):
    __tablename__ = 'invites'

    signed_up = db.Column(db.Boolean)
    phone_number = db.Column(db.String(255), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id', ondelete='CASCADE'))


class LoanRequest(BaseModel):
    __tablename__ = 'loanrequests'

    amount = db.Column(db.String(255), nullable=False)
    installment_amount = db.Column(db.String(255), nullable=True)
    referral = db.Column(db.String(255), nullable=True)
    id_type = db.Column(db.String(255), nullable=False)
    id_number = db.Column(db.String(255), nullable=False)
    interest_rate = db.Column(db.String(255), nullable=True)
    processing_officer = db.Column(db.String(255), nullable=True)
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(255), nullable=True)
    phoneNumber = db.Column(db.String(255), nullable=True)
    momoNumber = db.Column(db.String(255), nullable=True)
    mno = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    paymentPlan = db.Column(db.String(255), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id', ondelete='CASCADE'))
    payments = db.relationship('LoanPayments', backref='loanrequest', cascade='all, delete-orphan')


class LoanPayments(BaseModel):
    __tablename__ = 'loanpayments'

    amount_paid = db.Column(db.String(255), nullable=False)
    amount_remaining = db.Column(db.String(255), nullable=False)
    loan_request_id = db.Column(db.Integer, db.ForeignKey('loanrequests.id', ondelete='CASCADE'))
    paymentPlan = db.Column(db.String(255), nullable=True)




    
