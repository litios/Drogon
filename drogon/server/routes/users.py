import sys
import random
import secrets
import datetime

sys.path.insert(1, '../')

from manager import Manager
from crypto_tool import Encryptor
from cryptography.fernet import InvalidToken
from connexion import NoContent
from flask import request
from flask.views import MethodView
from pathlib import Path
from pymongo import MongoClient

def check_auth(token, username):
    db_client = MongoClient('mongodb://localhost:27017/drogon')
    passwd, salt = token.split('-')
    encryptor = Encryptor(passwd.encode(), str(salt).encode())

    db = db_client['drogon']
    users = db['users']

    user_data = users.find_one({'username': username})

    decrypted = encryptor.decrypt_passwd(user_data['token_user_data']).decode()

    if username in decrypted:
        data = decrypted.split('-')
        return data[1], data[2]
    else:
        return False

class LoginView(MethodView):
    db_path = '../../drogon/{username}.dr'
    db_client = MongoClient('mongodb://localhost:27017/drogon')

    def put(self):
        user_data = request.json
        if Path(self.db_path.format(username = user_data['username'])).is_file():
            return 'Username already in use', 401
        
        open(self.db_path.format(username = user_data['username']), 'w+').close()

        db = self.db_client['drogon']
        users = db['users']
        users.insert_one({
            'username' : user_data['username'],
            'token_user_data': '',
            'token_datetime': datetime.datetime.utcnow()
        })

        return 'ok'


    def post(self):
        user_data = request.json

        if not Path(self.db_path.format(username = user_data['username'])).is_file():
            return 'User doesn\'t exist', 401
        
        try:
            Manager(self.db_path.format(username = user_data['username']), user_data['master_passwd'].encode(), str(user_data['master_number']).encode())
        except InvalidToken:
            return 'Invalid credentials', 400

        passwd = secrets.token_hex(256)
        salt = random.randint(1, 500000)

        encryptor = Encryptor(passwd.encode(), str(salt).encode())
        token = passwd + '-' + str(salt)
        encrypted_to_bbdd = encryptor.encrypt_passwd(user_data['username'] + '-' + user_data['master_passwd'] + '-' + str(user_data['master_number'])).decode()

        db = self.db_client['drogon']
        users = db['users']
        users.update_one({'username': user_data['username']}, {"$set": {
            'token_user_data': encrypted_to_bbdd,
            'token_datetime': datetime.datetime.utcnow()
        }})

        return token
        