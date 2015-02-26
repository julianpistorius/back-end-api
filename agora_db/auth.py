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
        self.auth_key = s.loads(self.auth_header['X-AUTH-KEY'])
        # self.user_key = self.auth_header['X-AUTH-USER']
        user = AgoraUser()
        user.id = self.auth_key
        user.get_user()
        self.is_authorized_user = user.id == self.auth_key  # users auth key is valid

    def is_user_owner(self, user_id):
        pass