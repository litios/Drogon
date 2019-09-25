from manager import Manager
from pathlib import Path
from getpass import getpass
from cryptography.fernet import InvalidToken
import sys
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\u001b[36;1m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

if __name__ == '__main__':
    print(bcolors.OKBLUE + bcolors.BOLD +'\n ----------------------------------------------------------------------------')
    print(' --------------------- DROGON KEEPS YOUR PASSWORDS SAFE ---------------------')
    print(' ----------------------------------------------------------------------------')
    print('\n\n\t            ..                                              \n\t        .-".\'                      .--.            _..._    \n\t      .\' .\'                     .\'    \       .-""  __ ""-. \n\t     /  /                     .\'       : --..:__.-""  ""-. \n\t    :  :                     /         ;.d$$    sbp_.-""-:_:\n\t    ;  :                    : ._       :P .-.   ,"TP        \n\t    :   \                    \  T--...-; : d$b  :d$b        \n\t     \   `.                   \  `..\'    ; $ $  ;$ $        \n\t      `.   "-.                 ).        : T$P  :T$P        \n\t        \..---^..             /           `-\'    `._`._     \n\t       .\'        "-.       .-"                     T$$$b    \n\t      /             "-._.-"               ._        \'^\' ;   \n\t     :                                    \.`.         /    \n\t     ;                                -.   \`."-._.-\'-\'     \n\t    :                                 .\'\   \ \ \ \         \n\t    ;  ;                             /:  \   \ \ . ;        \n\t   :   :                            ,  ;  `.  `.;  :        \n\t   ;    \        ;                     ;    "-._:  ;        \n\t  :      `.      :                     :         \/         \n\t  ;       /"-.    ;                    :                    \n\t :       /    "-. :                  : ;                    \n\t :     .\'        T-;                 ; ;        \n\t ;    :          ; ;                /  :        \n\t ;    ;          : :              .\'    ;       \n\t:    :            ;:         _..-"\     :       \n\t:     \           : ;       /      \     ;      \n\t;    . \'.         \'-;      /        ;    :      \n\t;  \  ; :           :     :         :    \'-.      \n\t\'.._L.:-\'           :     ;          ;    . `. \n\t                     ;    :          :  \  ; :  \n\t                     :    \'-..       \'.._L.:-\'  \n\t                      ;     , `.                \n\t                      :   \  ; :                \n\t                      \'..__L.:-\'\'')
    
    db_path = input(bcolors.ENDC + bcolors.BOLD + '\n Enter passwords\' file path: ')
    db_path += '.dr'
    if not Path(db_path).is_file():
        new = input(bcolors.FAIL + bcolors.BOLD + '\n That file does not exist. Do you want to create it? (y/n) '+ bcolors.ENDC)
        if new != 'y':
            print('Bye')
            sys.exit(0)
        open(db_path, 'w+').close()
        print(bcolors.OKGREEN + bcolors.BOLD + ' File created successfully.' + bcolors.ENDC)

    passwd = getpass(bcolors.WARNING + bcolors.BOLD + ' Enter your master passwd: ' + bcolors.ENDC)
    value = int(getpass(bcolors.WARNING + bcolors.BOLD + ' Enter your secret number: ' + bcolors.ENDC))

    master_passwd = passwd[:(value % len(passwd))].encode()
    salt = passwd[(value % len(passwd)):].encode()

    try:
        manager = Manager(db_path, master_passwd, salt)
        print(bcolors.OKGREEN + bcolors.BOLD + ' Access granted' + bcolors.ENDC)
    except InvalidToken:
        print(bcolors.FAIL + bcolors.BOLD + ' \nWrong password' + bcolors.ENDC)
        sys.exit(0)

    while True:
        option = input(bcolors.BOLD + '\n Store password (s), read password (r), list passwords (l) or exit (e): '+ bcolors.ENDC)

        if option == 's':
            while True:
                name = input(bcolors.BOLD +' Enter name of the password: '+ bcolors.ENDC)
                if manager.check_if_exists(name):
                    print(bcolors.FAIL +' That name already exists.'+ bcolors.ENDC)
                else:
                    break
            passwd = getpass(bcolors.BOLD +' Enter the password: '+ bcolors.ENDC)
            manager.store_passwd(name, passwd)
            print(bcolors.OKGREEN + bcolors.BOLD + ' Password stored successfully' + bcolors.ENDC)

        elif option == 'r':
            name = input(bcolors.BOLD + ' Enter name of the password: ' + bcolors.ENDC)
            if manager.check_if_exists(name):
                print(bcolors.BOLD + '\n ' + bcolors.UNDERLINE + manager.get_passwd(name).decode() + bcolors.ENDC)
            else:
                print(bcolors.FAIL + bcolors.BOLD + ' That password\'s name doesn\'t exist' + bcolors.ENDC)
        elif option == 'l':
            print(bcolors.BOLD + bcolors.OKGREEN +  '\n Passwords stored:' + bcolors.ENDC)
            for item in manager.list_passwd():
                print(bcolors.BOLD + ' ' + item + bcolors.ENDC)
        elif option == 'e':
            sys.exit(0)
        else:
            print(bcolors.BOLD + bcolors.FAIL +' Option not valid.' + bcolors.ENDC)
    
