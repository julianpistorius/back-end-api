__author__ = 'marnee'
import falcon
from db.auth import Auth
from db.conversation import Conversation
from base import ApiBase
from validators.validate_conversation_response_schema import validate_conversation


class ApiConversation(ApiBase):
    def on_get(self, request, response, user_id=None, group_id=None, conversation_id=None):
        #TODO get a list of conversations for entity sorted by date
        #TODO get specified conversation for conversation_id
        #TODO check user (started or with) or group member (started or with)
        pass

    def on_post(self, request, response):
        if self.validate_json(request, validator=validate_conversation):
            #TODO create conversation
            response.status = falcon.HTTP_201
        else:
            response.status = falcon.HTTP_400

    def on_put(self, request, response, conversation_id):
        if self.validate_json(request, validator=validate_conversation):
            #TODO update conversation
            response.status = falcon.HTTP_200
        else:
            response.status = falcon.HTTP_400