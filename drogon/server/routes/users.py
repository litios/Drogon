import sys
import random
import secrets
import datetime
import jwt
import os

sys.path.insert(1, '../')

from manager import Manager
from crypto_tool import Encryptor
from cryptography.fernet import InvalidToken
from connexion import NoContent
from flask import request
from flask.views import MethodView
from pathlib import Path
from pymongo import MongoClient

class LoginView(MethodView):
    db_path = '../../drogon/{username}.dr'
    db_client = MongoClient('mongodb://localhost:27017/drogon')

    def put(self):
        user_data = request.json
        db = self.db_client['drogon']
        users = db['users']

        if Path(self.db_path.format(username = user_data['username'])).is_file() and users.find_one({'username': user_data['username']}):
            return 'Username already in use', 403
        
        open(self.db_path.format(username = user_data['username']), 'w+').close()

        
        users.insert_one({
            'username' : user_data['username'],
            'token_user_data': '',
            'token_datetime': datetime.datetime.utcnow()
        })

        return 'ok'


    def post(self):
        user_data = request.json

        if not Path(self.db_path.format(username = user_data['username'])).is_file():
            return 'User doesn\'t exist', 400
        
        try:
            Manager(self.db_path.format(username = user_data['username']), user_data['master_passwd'].encode(), str(user_data['master_number']).encode())
        except InvalidToken:
            return 'Invalid credentials', 400
        
        user_encrypt_data = {
            'username': user_data['username'],
            'passwd': secrets.token_hex(256),
            'salt': random.randint(1, 500000)
        }

        # Just for the username to not travel in plain text
        encoded_jwt = jwt.encode(user_encrypt_data, os.environ.get('jwt_encode_key'), algorithm='HS256')

        encryptor = Encryptor(user_encrypt_data['passwd'].encode(), str(user_encrypt_data['salt']).encode())
        encrypted_to_bbdd = encryptor.encrypt_passwd(user_data['master_passwd'] + '-' + str(user_data['master_number'])).decode()

        db = self.db_client['drogon']
        users = db['users']
        users.update_one({'username': user_data['username']}, {"$set": {
            'token_user_data': encrypted_to_bbdd,
            'token_datetime': datetime.datetime.utcnow()
        }})

        return encoded_jwt
        