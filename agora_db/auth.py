__author__ = 'Marnee Dearman'
import os
import time
import uuid
import simplejson
from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer, BadSignature, BadTimeSignature
import settings
from agora_db.user import AgoraUser

class Auth(object):
    def __init__(self, auth_header):
        self.auth_header = auth_header
        s = URLSafeSerializer(secret_key=settings.TOKEN_SECRET_KEY)
        self.auth_key = s.loads(self.auth_header['x-auth-key'])
        self.user_key = s.loads(self.auth_header['x-auth-user'])
        user = AgoraUser()
        user.id = self.user_key
        user.get_user()
        self.is_authorized_user = user.permanent_web_token == self.auth_key  # users auth key is valid

    def is_user_owner(self, user_id):
        pass
