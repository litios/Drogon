import sys
import random
import secrets

sys.path.insert(1, '../')

from manager import Manager
from crypto_tool import Encryptor
from cryptography.fernet import InvalidToken
from connexion import NoContent
from flask import request
from flask.views import MethodView
from pathlib import Path
from pymongo import MongoClient

    

class PasswordsView(MethodView):
    db_path = '../../drogon/{username}.dr'
    db_client = MongoClient('mongodb://localhost:27017/drogon')
    
    def get_manager(self, user):
        value = int(len(user['passwd']) / 2)

        return Manager(self.db_path.format(username = user['username']), user['passwd'][:value].encode(), user['passwd'][value:].encode())

    def post(self, user):
        user_data = request.json
        manager = self.get_manager(user)
        return manager.get_passwd(user_data['identifier'])


    def put(self, user):
        user_data = request.json
        manager = self.get_manager(user)
        manager.store_passwd(user_data['identifier'], user_data['password'])
        
        return user_data['identifier'] 

    def search(self, user):
        manager = self.get_manager(user)
        return [identifier for identifier in manager.list_passwd()]