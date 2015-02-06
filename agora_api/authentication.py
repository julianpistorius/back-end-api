__author__ = 'Marnee Dearman'
import os
import time
import uuid
import agora_api
import msgpack_pure
from agora_db.py2neo_user import AgoraUser
import simplejson

#TODO add authentication logic
class Login(object):
    def __init__(self):
        pass

    def on_post(self, request, response):
        #is login a post?
        pass

    def on_get(self, request, response):
        #is a login a get
        pass