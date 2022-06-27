from http import client
from flask import Flask, request, json
from dotenv import load_dotenv, find_dotenv
import os
import uuid
from datetime import datetime
import pprint
import json
from matplotlib import collections
from matplotlib.pyplot import xcorr
from numpy import append
from torch import int32
from pymongo import MongoClient, mongo_client
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import set_access_cookies
from flask_jwt_extended import unset_jwt_cookies

load_dotenv(find_dotenv())

password = os.environ.get("MONGODB_PWD")

connetion_string = "mongodb+srv://hansparson013:{}@cluster0.gzzetzc.mongodb.net/?retryWrites=true&w=majority".format(password)
client = MongoClient(connetion_string)

app = Flask(__name__)


# app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
# app.config["JWT_COOKIE_SECURE"] = True
app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)

dbs = client.list_database_names()
test_db = client.MNC_Group
    

@app.route('/register', methods=['POST'])
def register():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        first_name = json['first_name']
        last_name = json['last_name']
        phone_number = json['phone_number']
        address = json['address']
        pin = json['pin']
        
        try :
            collection = test_db.example_data
            # 
            test_document = {
                "user_id" : "{}".format(str(uuid.uuid4())),
                "first_name" : "{}".format(first_name),
                "last_name": "{}".format(last_name),
                "phone_number": "{}".format(phone_number),
                "address": "{}".format(address),
                "pin": "{}".format(pin),
                "amount": 0,
                "created_date": "{}".format(datetime.now().strftime("%m-%d-%Y %H:%M:%S"))
            }
            collection.create_index([('phone_number', 1)], unique=True)
            inserted_id =  collection.insert_one(test_document)
            succes_response = {
                "status": "SUCCESS",
                "result": {
                    "user_id" : "{}".format(str(uuid.uuid4())),
                    "first_name" : "{}".format(first_name),
                    "last_name": "{}".format(last_name),
                    "phone_number": "{}".format(phone_number),
                    "address": "{}".format(address),
                    "created_date": "{}".format(datetime.now().strftime("%m-%d-%Y %H:%M:%S"))
                }
            }
            return succes_response
        except :
            duplicate = {
                "message": "Phone Number already registered"
            }
            return duplicate
    else:
        return 'Content-Type not supported!'
    
    
@app.route('/login', methods=['POST'])
def login():
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        phone_number = json['phone_number']
        pin = json['pin']
        
        collection = test_db.example_data
        hasil = collection.find_one({"phone_number" : "{}".format(phone_number)})
        search_pin = hasil['pin']
        if pin == search_pin:
            access_token = create_access_token(identity={'phone_number': phone_number})
            refresh_token = create_refresh_token(identity={'phone_number': phone_number})
            result_acount = {
                "status": "SUCCESS",
                "result": {
                    "access_token": "{}".format(access_token),
                    "refresh_token": "{}".format(refresh_token)
                }
               }           

            return result_acount 
        else:
                result_acount = {
                    "message": "Phone number and pin doesn't match."
                }
                return result_acount  
    else:
        return 'Content-Type not supported!'
    
@app.route('/top_up', methods=['POST'])
@jwt_required()
def top_up():
    try:
        current_user = get_jwt_identity()
        content_type = request.headers.get('Content-Type')
        if (content_type == 'application/json'):
            json = request.json
            json_amount = json['amount']
            print(json_amount)
            collection = test_db.example_data
            hasil = collection.find_one(current_user)
            _id = hasil['_id']
            amount = hasil['amount']
            amount_after = amount + json_amount
            collection.update_one(current_user, {"$set": {'amount': amount_after}})

            top_up_uid = str(uuid.uuid4())
            tanggal_transaksi = datetime.now().strftime("%m-%d-%Y %H:%M:%S")
            user_id = hasil['user_id']
            
            transaction_db = test_db.transaction_data ### Untuk Database Transaksi
            top_up_db = {
                "top_up_id" : "{}".format(top_up_uid),
                "status" : "SUCCESS",
                "user_id": "{}".format(user_id),
                "Transacton_type": "CREDIT",
                "amount": json_amount,
                "remarks": "",
                "balance_before": amount,
                "balance_after": amount_after,
                "created_date": "{}".format(tanggal_transaksi)
            }
            transaction_db.insert_one(top_up_db)

            result_acount = {
                    "status": "SUCCESS",
                    "result": {
                        "top_up_id": "{}".format(top_up_uid),
                        "amount_top_up": json_amount,
                        "balance_before": amount,
                        "balance_after": amount_after,
                        "created_date": "{}".format(tanggal_transaksi)
                    }
                }
            return result_acount

    except:
        result_acount = {
                    "message": "Unauthenticated"
                }
        return result_acount 


@app.route('/payment', methods=['POST'])
@jwt_required()
def payment():
    current_user = get_jwt_identity()
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        json_amount = json['amount']
        json_remark = json['remarks']

        payment_id = str(uuid.uuid4())
        tanggal_transaksi = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

        collection = test_db.example_data
        hasil = collection.find_one(current_user)
        amount = hasil['amount']
        user_id = hasil['user_id']
        print(current_user)
        if amount - json_amount > 0 or amount - json_amount == 0:
            amount_after = amount - json_amount
            collection.update_one(current_user, {"$set": {'amount': amount_after}}) ##### Mengurangi salto setelah Transfer

            transaction_db = test_db.transaction_data ### Untuk Database Transaksi
            transfer = {
                "payment_id" : "{}".format(payment_id),
                "status" : "SUCCESS",
                "user_id": "{}".format(user_id),
                "Transacton_type": "DEBIT",
                "amount": json_amount,
                "remarks": "{}".format(json_remark),
                "balance_before": amount,
                "balance_after": amount_after,
                "created_date": "{}".format(tanggal_transaksi)
            }
            transaction_db.insert_one(transfer)

            result_acount = {
                "status": "SUCCESS",
                "result": {
                    "payment_id": "{}".format(payment_id),
                    "amount": json_amount,
                    "remarks": "{}".format(json_remark),
                    "balance_before": amount,
                    "balance_after": amount_after,
                    "created_date": "{}".format(tanggal_transaksi)
                }
            }
            return result_acount
        
        elif amount - json_amount < 0:
            result_acount = {
                    "message": "Balance is not enough"
                }
            return result_acount
        else:
            result_acount = {
                    "message": "Unauthentcated"
                }
            return result_acount


@app.route('/transfer', methods=['POST'])
@jwt_required()
def transfer():
    current_user = get_jwt_identity()
    content_type = request.headers.get('Content-Type')
    if (content_type == 'application/json'):
        json = request.json
        json_amount = json['amount']
        json_target_user = json['target_user']
        json_remark = json['remarks']
        print(json_target_user)

        transfer_id = str(uuid.uuid4())
        tanggal_transaksi = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

        collection = test_db.example_data
        hasil = collection.find_one(current_user)
        amount = hasil['amount']
        user_id = hasil['user_id']

        print(current_user)
        if amount - json_amount > 0 or amount - json_amount == 0:
            amount_after = amount - json_amount
            collection.update_one(current_user, {"$set": {'amount': amount_after}}) ##### Mengurangi salto setelah Transfer

            target_transfer = collection.find_one({'user_id': '{}'.format(json_target_user)})
            phone_target = target_transfer['amount']
            amount_target = target_transfer['amount']
            print(phone_target)
            amount_target = amount_target + json_amount
            collection.update_one({'user_id': '{}'.format(json_target_user)}, {"$set": {'amount': amount_target}})

            transaction_db = test_db.transaction_data ### Untuk Database Transaksi
            transfer = {
                "transfer_id" : "{}".format(transfer_id),
                "status" : "SUCCESS",
                "user_id": "{}".format(user_id),
                "Transacton_type": "DEBIT",
                "amount": json_amount,
                "remarks": "{}".format(json_remark),
                "balance_before": amount,
                "balance_after": amount_after,
                "created_date": "{}".format(tanggal_transaksi)
            }
            transaction_db.insert_one(transfer)

            result_acount = {
                "status": "SUCCESS",
                "result": {
                    "payment_id": "{}".format(transfer_id),
                    "amount": json_amount,
                    "remarks": "{}".format(json_remark),
                    "balance_before": amount,
                    "balance_after": amount_after,
                    "created_date": "{}".format(tanggal_transaksi)
                }
            }
            return result_acount
        
        elif amount - json_amount < 0:
            result_acount = {
                    "message": "Balance is not enough"
                }
            return result_acount
        else:
            result_acount = {
                    "message": "Unauthen<cated"
                }
            return result_acount
            


@app.route('/transactions', methods=['GET'])
@jwt_required()
def transactions():
    current_user = get_jwt_identity()
    collection = test_db.example_data
    hasil = collection.find_one(current_user)
    user_id = hasil['user_id']

    transaction_db = test_db.transaction_data
    transaction = transaction_db.find({"user_id":"{}".format(user_id)}, {"_id": False})
    list_transaction = ""
    for x in transaction:
        list_transaction = list_transaction + ", " + str(x)

    ######### Manipulasi String bisa bisa jadi JSON #########    
    list_transaction = list_transaction[2:]
    list_transaction = "[" + list_transaction + "]"
    list_transaction = list_transaction.replace("'", '"')
    json_obj = json.loads(list_transaction)

    print(list_transaction)
    # list_transaction = list_transaction.replace("'", '"')
    hasil = {
        "status" : "SUCCESS",
        "result" : json_obj
    }
    return hasil


@app.route('/profile', methods=['PUT'])
@jwt_required()
def profile():
    current_user = get_jwt_identity()
    first_name = request.json['first_name']
    last_name = request.json['last_name']
    address = request.json['address']

    collection = test_db.example_data
    hasil = collection.find_one(current_user)
    user_id = hasil['user_id']
    tanggal_update = datetime.now().strftime("%m-%d-%Y %H:%M:%S")

    collection.update_one({'user_id': '{}'.format(user_id)}, {"$set": {'first_name': first_name, 'last_name': last_name, 'address': address}})

    hasil = {
        "status" : "SUCCESS",
        "result": {
                    "user_id": "{}".format(user_id),
                    "first_name": "{}".format(first_name),
                    "last_name": "{}".format(last_name),
                    "address": "{}".format(address),
                    "updated_date": "{}".format(tanggal_update)
                }
    }
    
    return hasil

if __name__ == "__main__":
    app.run()
    