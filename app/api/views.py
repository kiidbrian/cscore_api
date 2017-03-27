from flask import render_template, session, redirect, url_for, request, flash
from flask import jsonify
from config import config
from threading import Thread
from werkzeug.utils import secure_filename
from . import api
from datetime import datetime
from app import db
from models import *
import re
import json
import requests

@api.route('/login', methods=['POST'])
def login():
    try:
        json_payload = request.get_json()
        
        phone_number = json_payload['phoneNumber']
        pin = json_payload['pin']

        phone_number = handle_msisdn(phone_number)

        if phone_number !='' and pin !='':
            # phone_number = handle_msisdn(msisdn)
            client = Client.query.filter_by(phone_number=phone_number).first()
            # print(client)
            if client is not None and client.verify_pin(pin):
                print(client.id)
                data = {
                    "id": client.id,
                    "fullname": client.fullname,
                    "occupation": client.occupation,
                    "age": int(client.age),
                    "weeklyIncome": float(client.weekly_income),
                    "phoneNumber": client.phone_number,
                    "homeAddress": client.home_address,
                    "workAddress": client.work_address,
                    "status": client.status
                }
                print(data)
                return jsonify(code=config['SUCCESS'], message="success", data=data)
            return jsonify(code=config['FAILURE'], message="Invalid phone number or pin")
        return jsonify(code=config['ERROR'], message="Bad request")
    except Exception as e:
        return jsonify(code=config['ERROR'], message=str(e))


@api.route('/register', methods=['POST'])
def register():
    try:
        json_payload = request.get_json()
        # print(json_payload)
        firstname = json_payload['firstName']
        lastname = json_payload['lastName']
        occupation = json_payload['occupation']
        age = json_payload['age']
        weekly_income = json_payload['weeklyIncome']
        phone_number = json_payload['phoneNumber']
        home_address = json_payload['homeAddress']
        work_address = json_payload['workAddress']
        pin = json_payload['pin']

        phone_number = handle_msisdn(phone_number)

        check_phone_number = re.match(r'(^233+\d{9}$)', phone_number)

        if check_phone_number is not None:
            if firstname !='' and lastname !='' and occupation !='' and age!='' and weekly_income !='' and phone_number !='' and home_address !='' and pin !='':
                fullname = "{} {}".format(firstname, lastname)

                prediction = predict_status(occupation, weekly_income, age)
                
                client = Client()
                client.fullname = fullname
                client.occupation = occupation #hairdresser”, “mechanic”, ”trader” and “livestock”.
                client.age = age
                client.weekly_income = weekly_income
                client.phone_number = phone_number
                client.home_address = home_address
                client.work_address = work_address
                client.pin = pin
                client.status = prediction['data']

                db.session.add(client)
                db.session.commit()

                # send send
                sender_id = "CreditScore"
                recipient = phone_number
                message = "Welcome, {0}, You have been successfully registered on CreditScore. Your loan is a few moments away!".format(firstname) 
                
                sms_thread = Thread(target=send_sms, args=(sender_id, recipient, message))
                sms_thread.start()
                print("...SMS Thread started...")
                return jsonify(code=config['SUCCESS'], message="success")
            return jsonify(code=config['ERROR'], message="Bad request")
        return jsonify(code=config['ERROR'], message="Invalid phone format")
    except Exception as e:
        return jsonify(code=config['ERROR'], message=str(e))


@api.route('/apply', methods=['POST'])
def apply():
    try:
        json_payload = request.get_json()

        description = json_payload['description']
        amount = json_payload['amount']
        momoNumber = handle_msisdn(json_payload['momoNumber'] )
        network = json_payload['network']
        payment_plan = json_payload['paymentPlan']
        id_type = json_payload['idType']
        id_number = json_payload['idNumber']
        referral = json_payload['referral']
        client_id = int(json_payload['client_id'])

        check_phone_number = re.match(r'(^233+\d{9}$)', momoNumber)
        if check_phone_number is not None:
            client = Client.query.filter_by(id=int(client_id)).first()
            
            loan_request = LoanRequest(description=description, client_id=client.id, momoNumber=momoNumber, mno=network, \
            paymentPlan=payment_plan, id_type=id_type, id_number=id_number, referral=referral, amount=amount)

            db.session.add(client)
            db.session.add(loan_request)
            db.session.commit()

            return jsonify(code=config['SUCCESS'], message="Success")
        return jsonify(code=config['ERROR'], message="Invalid momoNumber format")

    except Exception as e:
        return jsonify(code=config['ERROR'], message=str(e))

def handle_msisdn(msisdn):
    m = str(msisdn)
    for x in range(len(m)):
        if x == 0:
            if m[x] == "0":
                return "233"+str(m[1:])
            else:
                return m
    

def predict_status(occupation, income, age):
    """
    Method to Predict Status of client
    Parameters: occupation, income, age
    Return: dict
    """
    try:
        url = "http://ec2-52-89-184-99.us-west-2.compute.amazonaws.com:5000/api/v1/predict"
        data = {
            "occupation": occupation,
            "income": float(income),
            "age": float(age)
        }
        request = requests.post(url, json.dumps(data)).json()
        return request
    except Exception as e:
        print(str(e))


def send_sms(sender_id, recipient, message):
    """
    Method to send SMS
    Parameters: sender_id, recipient, message
    Return: Boolean
    """
    try:
        url = config['SMS_PROVIDER']
        data = {
            'key': config['SMS_API_KEY'], 
            'contacts': [recipient],
            'senderid': sender_id, 
            'message': message, 
            'schedule_date': "now", 
            'schedule_time': "" 
        }
        headers  = {
            'Content-Type': 'application/json'
        }
        response = requests.post(url, data=json.dumps(data), headers=headers).json()
        # print(response)
        if response["status"] == "1000":
            return True
        return False
    except Exception as e:
        print(e)


def send_momo_prompt(phone_number, amount, mno, name, prompt_type):
    """
    Method to debit or credit a mobile money user
    Parameters: phoneNumber, amount, mno, name, type
    Return: dict
    """
    try:
        url = config['MOMO_PROVIDER']
        headers = {
            "X-Api-Key": config['MOMO_API_KEY']
        }
        data = {
            'phoneNumber': phone_number, 
            'amount': amount,
            'mno': mno, 
            'name': name, 
            'type': prompt_type
        }

        response = requests.post(url, data=json.dumps(data), headers=headers).json()
        if response["status"] == "success":
            return True
        return False
    except Exception as e:
        print(e)
        return False
    