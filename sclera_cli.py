#! /usr/bin/python3.6
from core import UsersClass
from os import system
import logging
from terminaltables import AsciiTable


class ScleraCLI(object):
    def __init__(self):
        self.cls = lambda: system('clear')
        self.inp = lambda mess: input(mess).strip()
        self.table = lambda items: print(AsciiTable(items).table)

    def header(self):
        self.cls()
        print(f'{"#"*34}\n#\t Sclera system cli\t #\n{"#"*34}\n')

    def menu(self):
        self.header()
        menu = {0: ['Exit', quit],
                1: ['Add admin', self.add_admin],
                2: ['Add user', self.add_user],
                3: ['Show users', self.show_users],
                4: ['Reset password', self.reset_password],
                5: ['Delete user', self.delete_user]}
        table = [['Key', 'Description']]
        for m in menu:
            table.append([m, menu[m][0]])
        self.table(table)
        try:
            menu.get(int(input('Choise:')))[1]()
            input('Press any key...')
            self.menu()
        except KeyboardInterrupt as ex:
            quit()

    def show_users(self):
        self.header()
        table = [['Login', 'status_user']]
        for contact in user.show_all_users('admin', 'user'):
            table.append([contact['login'], contact['status']['status_user']])
        self.table(table)

    def delete_user(self):
        login = self.inp('Username:')
        rez = user.delete_user(login)
        print(rez)

    def reset_password(self):
        login = self.inp('Username:')
        pwd = self._check_password()
        if pwd:
            rez = user.change_user_password(login, pwd)
            print(rez)
        else:
            print('Error reset password')

    def _check_password(self):
        password = self.inp('Password:')
        conf_password = self.inp('Retry:')
        return password if password == conf_password else False

    def add_user(self):
        login = self.inp('Username:')
        pwd = self._check_password()
        if pwd:
            rez = user.add_new_user(login, pwd, 'user')
            print(rez)
        else:
            print('Error add user')

    def add_admin(self):
        login = self.inp('Username:')
        pwd = self._check_password()
        if pwd:
            rez = user.add_new_user(login, pwd, 'admin')
            print(rez)
        else:
            print('Error add admin')


if __name__ == '__main__':
    logging.critical('start')
    user = UsersClass()
    sclera = ScleraCLI()
    sclera.menu()
