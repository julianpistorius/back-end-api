__author__ = 'Marnee Dearman'
import uuid
import settings
from py2neo import Node, Graph, Relationship
from user import AgoraUser
from agora_services import smtp
from agora_types import AgoraRelationship, AgoraLabel
from itsdangerous import (TimedJSONWebSignatureSerializer as TokenSerializer, SignatureExpired, BadSignature)

# config = importlib.import_module('config')

class AgoraRegisterUser(object):
    def __init__(self):
        self.graph_db = Graph(settings.DATABASE_URL)

    def register_user(self, email):
        user = AgoraUser()
        user.email = email
        user.get_user()
        message = smtp.AgoraSmtp()
        web_token = TokenSerializer(secret_key="devkey")
        message.recipients = email
        if user.id == '':
            #send registration message
            user.temporary_web_token = web_token
            #TODO setup message with URL and token
            message.send_by_gmail()
            #if successful
            user.create_user()
        else:
            #send login message
            user.permanent_web_token = web_token
            message.send_by_gmail()
            #if successful
            user.update_user()

    def construct_url(self):
        pass




# 1 check for existing user by email
# 2 check for current web token
# 3 generate & store temporary token
# 4 send email with link

