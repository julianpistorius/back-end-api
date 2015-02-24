__author__ = 'Marnee Dearman'
import os
import time
import uuid
import agora_api
from agora_db import user
import simplejson
from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer, BadSignature, BadTimeSignature
import settings

#TODO add authentication logic
class Auth(object):
    def __init__(self, auth_header, id):
        self.auth_header = auth_header
        self.user_id = id

    def is_authorized_user(self):
        s = URLSafeSerializer(secret_key=settings.TOKEN_SECRET_KEY)
        auth_payload = s.loads(self.auth_header['x-auth-key'])
        if self.user_id == auth_payload:
            return True
