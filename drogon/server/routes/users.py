import sys
import random
import secrets

sys.path.insert(1, '../')

from manager import Manager
from crypto_tool import Encryptor
from cryptography.fernet import InvalidToken

def login(user_data):
    user_data = request.get_json(force=True)
    try:
        Manager('../../drogon/vault.dr', user_data['master_passwd'], user_data['master_number'])
    except InvalidToken:
        return 'Invalid credentials', 400

    passwd = secrets.token_hex(256)
    salt = random.randint(1, 500000)

    encryptor = Encryptor(passwd, salt)
    token = passwd + '-' + str(salt)

    print(encryptor.encrypt_passwd( user_data['master_passwd'] + '-' + user_data['master_number']))
    return token
    