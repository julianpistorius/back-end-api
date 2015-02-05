__author__ = 'Marnee Dearman'
import uuid
from py2neo import Node, Graph, Relationship
from agora_db.py2neo_user import AgoraUser
from agora_types import AgoraRelationship, AgoraLabel
from itsdangerous import (TimedJSONWebSignatureSerializer as TokenSerializer, SignatureExpired, BadSignature)


# config = importlib.import_module('config')


class AgoraRegisterUser(object):
    def __init__(self):
        self.graph_db = Graph()

    def register_user(self, email):
        user = AgoraUser()
        user.email = email
        user.get_user()
        if user.id == '':
            #send welcome message
        else:
            #send login message


    def check_token(self, token):
        pass

    def find_user_by_email(self):
        pass

    def get_temporary_token(self):
        pass

    def construct_url(self):
        pass


# 1 check for existing user by email
# 2 check for current web token
# 3 generate & store temporary token
# 4 send email with link

