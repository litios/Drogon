
from crypto_tool import Encryptor
from flask import request
from pymongo import MongoClient
from cryptography.fernet import InvalidToken
from datetime import datetime
import jwt
import os

db_client = MongoClient('mongodb://localhost:27017/drogon')
db = db_client['drogon']
users = db['users']

def clean_token(username):
    users.update_one({'username': username}, {'$set': {'token_user_data' : ''}})

def check_auth(token):
    user_encryption_data = {}
    try:
        user_encryption_data = jwt.decode(token, os.environ.get('jwt_encode_key'), algorithms=['HS256'])
    except jwt.exceptions.InvalidTokenError:
        return None

    encryptor = Encryptor(user_encryption_data['passwd'][:180].encode(), user_encryption_data['passwd'][180:].encode())
    user_data = users.find_one({'username': user_encryption_data['username']})

    if user_data == None or user_data['token_user_data'] == '':
        clean_token(user_encryption_data['username'])
        return None

    # If the time since the token was obtained is more than 5 minutes, reset the token
    if (datetime.utcnow() - user_data['token_datetime']).total_seconds() > 300:
        clean_token(user_encryption_data['username'])
        return None

    try:
        decrypted = encryptor.decrypt_passwd(user_data['token_user_data']).decode()
    except InvalidToken:
        clean_token(user_encryption_data['username'])
        return None

    users.update_one({'username': user_encryption_data['username']}, {'$set': {'token_datetime' : datetime.utcnow()}})

    return {'uid': {'username': user_encryption_data['username'], 'passwd': decrypted}}
