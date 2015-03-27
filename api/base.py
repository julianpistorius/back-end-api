__author__ = 'marnee'
# from abc import ABCMeta, abstractmethod
import simplejson
from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer, BadSignature, BadTimeSignature, BadPayload
import settings
from db.user import User
import sys


class ApiBase():
    def __init__(self):
        self.is_authorized_user = False
        self.user_id = None
        self.result_json = None

    def validate_json(self, request, validator):
        raw_json = request.stream.read()
        result_json = simplejson.loads(raw_json, encoding='utf-8')
        if validator(result_json):
            self.result_json = result_json
            return True
        else:
            return False

    def authorize_user(self, request):
        x_auth_key = request.headers['X-AUTH-KEY']
        serializer = URLSafeSerializer(secret_key=settings.TOKEN_SECRET_KEY)
        try:
            user = User()
            user.id = serializer.loads(x_auth_key)
            self.is_authorized_user = user.get_user()
            self.user_id = user.id
            return self.is_authorized_user
        except BadSignature:
            return False
        except BadPayload:
            return False
        except:
            print sys.exc_info()[0]
            return False

    @staticmethod
    def get_user_by_id(user_id):
        agora_user = User()
        agora_user.id = user_id
        agora_user.get_user()
        return agora_user

    @staticmethod
    def get_user_by_email(email):
        agora_user = User()
        agora_user.email = email
        agora_user.get_user()
        return agora_user


