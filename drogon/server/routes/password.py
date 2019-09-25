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

class PasswordView(MethodView):
    
    def get(self):
        pass