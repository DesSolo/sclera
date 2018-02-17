# -*- coding: utf-8 -*-
import pymongo
from hashlib import sha256
from secrets import token_urlsafe
from re import match
import configparser
from bson.objectid import ObjectId
import logging
import datetime
from urllib.parse import quote
import os

to_sha = lambda x: sha256(x.encode('utf-8')).hexdigest()
config = configparser.ConfigParser()
config.read('config.conf')
logging.basicConfig(filename=config.get('Logs', 'log_file'),
                    level=logging.INFO,
                    format='%(asctime)s,%(levelname)s,%(message)s',
                    datefmt='%d-%m-%y %H:%M')

def week():
    today = datetime.date.today()
    monday = today - datetime.timedelta(days=today.weekday())
    return [date.strftime('%Y-%m-%d') for date in [monday + datetime.timedelta(days=day) for day in range(7)]]

class Config(object):
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.conf')


class DataBase(object):
    def __init__(self, collection):
        client = pymongo.MongoClient()
        db = client[config.get('DataBase', 'name')]
        self.col = db[collection]

    def show_single(self, params={}, **kwargs):
        return self.col.find_one({**params}, {'_id': 0, **kwargs})

    def show_all(self, params={}, **kwargs):
        return [_ for _ in self.col.find({**params}, {'_id': 0, **kwargs}).limit(100)]

    def push(self, params=None, **kwargs):
        self.col.update_one({**params}, {'$push': {**kwargs}})


class TaskClass(DataBase):
    def __init__(self):
        super(TaskClass, self).__init__(config.get('DataBase', 'collection_tasks'))

    def show_single(self, params={}, **kwargs):
        return self.col.find_one({**params}, {'tmp': 0, **kwargs})

    def show_all(self, params={}, **kwargs):
        return [_ for _ in self.col.find({**params}, {'tmp': 0, **kwargs}).limit(100)]

    def show_week(self, login):
        td = datetime.datetime.now()
        start = td - datetime.timedelta(days=td.weekday())
        end = start + datetime.timedelta(days=6)
        return self.show_all({'login': login, 'cr_date': {'$lte': start, '$gte': end}}, user=0)

    def close(self, _id):
        return self.col.update_one({'_id': ObjectId(_id)}, {'$set': {'status': 'closed'}})

    def add_task(self, user, exp_date, description, image=''):
        """
        {
         "cr_date": "2017-11-25 22:38:05.399357",
          "exp_date": "2017-11-25 22:38:05.399357",
          "status": "new",
          "image": "/book_covers_step_13.png",
          "description": "Проснуться"
        }
        :return:
        """
        return self.col.insert_one({"user": user, "cr_date": datetime.datetime.now(), "exp_date": exp_date,
                                    "status": 'new', 'image': image, 'description': description}).inserted_id


class UsersClass(DataBase):
    def __init__(self):
        super(UsersClass, self).__init__(config.get('DataBase', 'collection'))

    def add_new_user(self, login, password, status='user'):
        if match(r'^[\w\d._]{4,20}$', login):
            if not self.show_single_user(login):
                rez = self.col.insert_one(
                    {'login': login, 'password': to_sha(password), 'status': {'status_user': status}})
                logging.critical(rez)
                return True
        else:
            return False

    def delete_user(self, login):
        self.col.delete_one({'login': login})

    def change_user_status(self, login, status):
        self.col.update_one({'login': login}, {'$set': {'status.status_user': status}})

    def auth_token(self, login, password):
        password = to_sha(password)
        user = self.show_single({'login': login, 'password': password})
        if user:
            status = user['status']['status_user']
            if status == 'user':
                token = token_urlsafe(18)
            elif status == 'moderator':
                token = token_urlsafe(19)
            elif status == 'admin':
                token = token_urlsafe(20)
            self.col.update_one({'login': login, 'password': password}, {'$set': {'token': token}})
            return token

    def change_user_password(self, login, new_password):
        self.col.update_one({'login': login}, {'$set': {'password': to_sha(new_password)}})

    def show_single_user(self, login, **kwargs):
        return self.show_single({'login': login}, password=0, **kwargs)

    def show_all_users(self, *args, **kwargs):
        return self.show_all({'status.status_user': {'$in': args}}, password=0, pays=0, token=0, **kwargs)

    def push_history(self, login, **kwargs):
        self.push_user(login, history={'date': datetime.now(), **kwargs})

    def set_user(self, login, **kwargs):
        self.col.update_one({'login': login}, {'$set': {**kwargs}})

    def push_user(self, login, **kwargs):
        self.col.update_one({'login': login}, {'$push': {**kwargs}})

    def search_users(self, source, **kwargs):
        if source:
            source = {'$regex': source}
            return self.show_all({'$or': [{'login': source}, {'email': source}, {'phone': source},
                                          {'login_inst': source}]}, password=0, token=0, **kwargs)
        else:
            return []


class PicturesClass(object):
    def __init__(self):
        self.path = config.get('Main', 'path_static_files')
        self.url_static_files = config.get('Main', 'url_static_files')
        self.col_files, self.col_pages, self.files = self.fond_files()
        logging.critical(self.col_pages, self.col_files)

    def fond_files(self):
        files = []
        for file in os.listdir(self.path):
            if os.path.isfile(os.path.join(self.path, file)):
                files.append(self.url_static_files + quote(file))
        pages = [[item for item in items] for items in zip(*[iter(files)] * 12)]
        return len(files), len(pages), pages

    def get_page(self, num):
        num = int(num)
        if num <= self.col_pages:
            return self.files[num]
        else:
            return []

a=PicturesClass()
b = a.get_page(2)
print(b)