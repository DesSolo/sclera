# -*- coding: utf-8 -*-
from tornado import web, ioloop
from json import dumps
import core

import logging


class BaseHendler(web.RequestHandler):
    login = None
    status = None

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def r_serv(self, **kwargs):
        return self.write(dumps({**kwargs}, ensure_ascii=False, default=str))

    def error(self, description):
        logging.error(f'{self.request.remote_ip} {description} {self.request.arguments}')
        return self.r_serv(status=False, description=description)

    def get(self, *args, **kwargs):
        raise web.HTTPError(404, 'Get method')


class TaskHandler(BaseHendler):
    def post(self, type, *args, **kwargs):
        if type == 'add':
            if self.status == 'admin':
                user = self.get_argument('login')
            else:
                user = Users.show_single({'token': self.get_argument('token')})['login']
            date = self.get_argument('date')
            description = self.get_argument('description')
            image = self.get_argument('image')
            task_id = Task.add_task(user, date, description, image)
            return self.r_serv(status=True, task=task_id, user=user)
        if type == 'my':
            user = Users.show_single({'token': self.get_argument('token')})['login']
            return self.r_serv(status=True, tasks=Task.show_all({'user': user}, user=0))
        else:
            return self.error('Bad arguments')

class UsersHandler(BaseHendler):
    def post(self, type, *args, **kwargs):
        status = Users.show_single(self.get_argument('token'))['status']['status_user']
        if status == 'admin':
            if type == 'add':
                login = self.get_argument('login')
                pwd = self.get_argument('pwd')
                rez = Users.add_new_user(login, pwd, 'user')
                if rez:
                    return self.r_serv(descriptin='Success add new user', status='OK')
                else:
                    return self.error('Error add new user')
            elif type == 'reset':
                login = self.get_argument('login')
                pwd = self.get_argument('pwd')
                rez = Users.change_user_password(login, pwd)
                if rez:
                    return self.r_serv(descriptin='Success change password', status='OK')
                else:
                    return self.error('Error change password')
            elif type == 'delete':
                login = self.get_argument('login')
                rez = Users.delete_user(login)
                if rez:
                    return self.r_serv(descriptin='Success delete user', status='OK')
                else:
                    return self.error('Error delete user')
            else:
                return self.error('Unknown type work')
        else:
            return self.error('User has no privileges')


class LoginHandler(BaseHendler):
    def post(self, *args, **kwargs):
        token = Users.auth_token(self.get_argument('login'), self.get_argument('password'))
        if token:
            user = Users.show_single_user(self.get_argument('login'))
            return self.r_serv(token=token, status=user['status']['status_user'])
        else:
            return self.error('Bad User')


class PicturesHandler(BaseHendler):
    def post(self, *args, **kwargs):
        user = Users.show_single(self.get_argument('token'))
        if user:
            return self.r_serv(images=Pics.get_files(self.get_argument('start'),self.get_argument('stop')))
        else:
            return self.error('Bad user')

application = web.Application([
    (r'/task/(.+)', TaskHandler),
    (r'/login', LoginHandler),
    (r'/users/(.+)', UsersHandler),
    (r'/images', PicturesHandler)])
application.listen('5000', xheaders=True)
Users = core.UsersClass()
Task = core.TaskClass()
Pics = core.PicturesClass()
ioloop.IOLoop.instance().start()
