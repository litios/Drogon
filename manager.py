from crypto_tool import Encryptor

class Manager:
    def __init__(self, db_route, master_passwd, salt):
        self.db_route = db_route
        self.encryption_tool = Encryptor(master_passwd, salt)

        with open(db_route, 'r+') as db:
            self.passwds = {}
            lines = db.readlines()
            for line in lines:
                name, passwd = line.split()
                self.passwds[self.encryption_tool.decrypt_passwd(name).decode()] = passwd

    def check_if_exists(self, name):
        return name in self.passwds

    def store_passwd(self, name, passwd):
        encrypted_passwd = self.encryption_tool.encrypt_passwd(passwd)
        encrypted_name = self.encryption_tool.encrypt_passwd(name)
        with open(self.db_route, 'a+') as db:
            db.write(encrypted_name.decode() + ' ' + encrypted_passwd.decode() + '\n')
        
        self.passwds[name] = encrypted_passwd.decode()

    def get_passwd(self, name):
        return self.encryption_tool.decrypt_passwd(self.passwds[name])

    def list_passwd(self):
        return self.passwds
