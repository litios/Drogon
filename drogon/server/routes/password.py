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
    
    def get(self, user):
        manager = Manager(self.db_path.format(username = user['username']), user['passwd'].encode(), str(user['salt']).encode())

        return manager.list_passwd()

    def post(self, user):
        manager = Manager(self.db_path.format(username = user['username']), user['passwd'].encode(), str(user['salt']).encode())

        return manager.list_passwd().items()


    def put(self, user):
        pass

    def search(self, limit=100):
      # NOTE: we need to wrap it with list for Python 3 as dict_values is not JSON serializable
      return []