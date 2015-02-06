__author__ = 'Marnee Dearman'
# import os
# import time
# import uuid
import falcon
# import msgpack_pure
from agora_db.py2neo_user import AgoraUser
from agora_db.py2neo_interest import AgoraInterest
import simplejson
from serializers import InterestResponder


class Interest(object):
    def __init__(self):
        pass


    def check_token(self):
        #TODO check tokens on api calls
        pass

    def on_get(self, request, response, interest_id):
        """
        get interest
        :param request:
        :param response:
        :param interest_id:
        :return:
        """
        response.data = self.get_interest(interest_id)
        response.content_type = 'application/json'
        response.status = falcon.HTTP_200

    def on_post(self, request, response, interest_id):
        """
        create interest
        :param request:
        :param response:
        :param interest_id:
        :return:
        """
        raw_json = request.stream.read()
        result_json = simplejson.loads(raw_json, encoding='utf-8')
        self.create_interest(result_json['interest'])
        response.status = falcon.HTTP_202

    def create_interest(self, interest_json):
        interest = AgoraInterest()
        interest.set_interest_attributes(interest_json)
        interest.create_interest()

    def get_interest(self, interest_id):
        interest = AgoraInterest()
        interest.id = interest_id
        interest.get_interest_by_id()
        interest_details = interest.get_interest_for_json()
        json = InterestResponder.respond(interest_details)
        return json
