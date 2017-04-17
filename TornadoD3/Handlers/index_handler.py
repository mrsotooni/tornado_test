#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import string
import os.path
import uuid
import jdatetime
from pycket.session import SessionManager
from models import *
import random


def authentication():
    def f(func):
        @functools.wraps(func)
        def func_wrapper(self, *args, **kwargs):
            if not self.current_user:
                self.redirect('/')
                return

            return func(self, *args, **kwargs)

        return func_wrapper

    return f


class TornadoRequestBase(tornado.web.RequestHandler):
    def __init__(self, application, request, **kwargs):
        super(TornadoRequestBase, self).__init__(application, request, **kwargs)

        self.session = SessionManager(self)

        self.user = {
            "name": self.session.get('name', None),
            "user": self.session.get('user', None),
            "id": self.session.get('id', None),
            "picture_address": self.session.get('picture_address', None),
            "id_admin": self.session.get('id_admin', None),
            "type_user": self.session.get('type_user', None),
            "online": self.session.get('online', None),
            "password": self.session.get('password', None),
            "email": self.session.get('email', None),
            "message": self.session.get('message', None),
            "count_message": self.session.get('count_message', None)


        }

    def get_current_user(self):
        return self.session.get('online')


class index_Handler(TornadoRequestBase):
    def get(self):
        self.render('home/index.html')

    def post(self, *args, **kwargs):
        username = self.get_argument('user')
        password = self.get_argument('password')
        # try:
        #     admin = Admin().select().where(Admin.user == username,Admin.password == password).get()
        # except:
        #     admin = False
        try:
            find_user = User().select().where((User.user == username) & (User.password == password) & ((User.status == 3) | (User.status==1))).get()
        except:
            find_user = False

        if find_user:
            try:
                message = Message().select().where(Message.id_reciver == find_user.id, Message.status == True)
                count_message = message.count()
                message_list = []
                m_dict = {}
                for item in message:
                    user = User().select().where(User.id == item.User).get()
                    m_dict = {'id':item.id,'description': item.description, 'status': item.status, 'name': user.name,
                              'picture_address': user.picture_address, 'date': str(item.date),"id":item.id}
                    message_list.append(m_dict)
            except:
                count_message = 0
                message_list = []

            self.session.set('name', find_user.name)
            self.session.set('id', find_user.id)
            self.session.set('id_admin', find_user.User)
            self.session.set('picture_address', find_user.picture_address)
            self.session.set('type_user', find_user.type)
            self.session.set('online', True)
            self.session.set('user', find_user.user)
            self.session.set('email', find_user.email)
            self.session.set('password', find_user.password)
            self.session.set('count_message', count_message)
            self.session.set('message', message_list)

            if find_user.type == True:
                self.write("admin-user")
            else:
                self.write('user')
        # elif admin:
        #     self.write("admin")
        else:
            self.write("نام کاربری یا پسورد اشتباه می باشد.یا اکانت شما فعال نیست.")


class register_Handler(TornadoRequestBase):
    def get(self):
        self.render('home/register.html')

class suggest_Handler(TornadoRequestBase):
    def get(self):
        self.render('home/suggest.html')
    def post(self):
        name = self.get_argument('name')
        email = self.get_argument('email')
        _suggest = self.get_argument('suggest')
        phone = self.get_argument('phonenumber')
        important = self.get_argument('important')
        su = suggest.create(
            name = name,
            email =email,
            important = important,
            suggest = _suggest
        )
#       self.render('home/suggest.html')
        self.write("<h2>succesfully</h2>")



class ForgetpassHandler(TornadoRequestBase):
    def get(self):
        self.render('home/forget_pass.html')




##################################