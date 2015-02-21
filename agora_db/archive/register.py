__author__ = 'Marnee Dearman'
import uuid
import settings
from py2neo import Node, Graph, Relationship
from user import AgoraUser
from agora_services import smtp
from agora_types import AgoraRelationship, AgoraLabel
# from itsdangerous import (TimedJSONWebSignatureSerializer as TimedTokenSerializer, SignatureExpired, BadSignature)
from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer, BadSignature

# config = importlib.import_module('config')

class AgoraRegisterUser(object):
    def __init__(self):
        self.graph_db = Graph(settings.DATABASE_URL)

    def register_user(self, email):
        user = AgoraUser()
        # user.id = id
        # user.email = email
        # user.get_user()
        verification_email = smtp.AgoraSmtp()
        # print web_token.dumps()
        verification_email.recipients = [user.email]
        s = URLSafeTimedSerializer(secret_key=settings.TOKEN_SECRET_KEY)
        payload = s.dumps(email)
        verification_email.subject = "Agora -- Verify Login/Registration"
        verification_email.message = self.construct_verification_url(payload=payload)
        verification_email.send_by_gmail()

    def construct_registration_url(self, json_time_web_token_serializer):
        pass

    def construct_verification_url(self, payload):
        return settings.SITE_URL + "/" + settings.ACTIVATION_ROUTE + "/%s" % payload

    #TODO complete registration from email URL
    def complete_registration(self):
        pass

class AgoraActivateUser(object):
    def __init__(self):
        self.graph_db = Graph(settings.DATABASE_URL)




# 1 check for existing user by email
# 2 check for current web token
# 3 generate & store temporary token
# 4 send email with link

