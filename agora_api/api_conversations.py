__author__ = 'marnee'
import falcon
from agora_db.auth import Auth
from agora_db.conversation import AgoraConversation
from validators import validate_conversation_response_schema
import simplejson


def user_auth(request):
    auth = Auth(auth_header=request.headers)
    return auth



class Conversation(object):
    def __init__(self):
        pass

    def on_get(self, request, response, user_id=None, group_id=None, conversation_id=None):
        #TODO get a list of conversations for entity sorted by date
        #TODO get specified conversation for conversation_id
        #TODO check user (started or with) or group member (started or with)
        pass

    def on_post(self, request, response):
        raw_json = request.stream.read()
        result_json = simplejson.loads(raw_json, encoding='utf-8')
        if validate_conversation_response_schema.validate_conversation(result_json):
            #TODO create conversation
            response.status = falcon.HTTP_201
        else:
            response.status = falcon.HTTP_400

    def on_put(self, request, response, conversation_id):
        raw_json = request.stream.read()
        result_json = simplejson.loads(raw_json, encoding='utf-8')
        if validate_conversation_response_schema.validate_conversation(result_json):
            #TODO update conversation
            response.status = falcon.HTTP_200
        else:
            response.status = falcon.HTTP_400