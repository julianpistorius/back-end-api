__author__ = 'marnee'
import sys
import falcon
from itsdangerous import BadSignature, BadTimeSignature
from agora_db.auth import Auth
from agora_db.meeting import AgoraMeeting
from api_serializers import MeetingResponder
import simplejson

def get_meeting_by_id(meeting_id):
    meeting = AgoraMeeting()
    meeting.id = meeting_id
    meeting.get_meeting()
    return meeting


def user_auth(request):
    auth = Auth(auth_header=request.headers)
    return auth


class Meeting(object):
    def __init__(self):
        pass

    def on_get(self, request, response, meeting_id=None):
        auth = user_auth(request)
        if meeting_id is not None:
            meeting = AgoraMeeting()
            meeting.id = meeting_id
            meeting.get_meeting()
            meeting_data = meeting.meeting_for_json(auth_key=auth.auth_key)
            response.data = MeetingResponder.respond(meeting_data,
                                                     linked={'groups': meeting_data['groups'],
                                                             'attendees': meeting_data['attendees']})
            response.content_type = 'application/json'
            response.status = falcon.HTTP_200

    def on_post(self, request, response, meeting_id=None):
        auth = user_auth(request)
        if auth.is_authorized_user:
            pass
        #TODO create new meeting

    def on_put(self, request, response, meeting_id):
        pass
        #TODO update meeting