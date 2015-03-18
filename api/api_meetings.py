__author__ = 'marnee'
import sys
import falcon
from itsdangerous import BadSignature, BadTimeSignature
from db.auth import Auth
from db.meeting import Meeting
from db.group import Group
from api_serializers import MeetingResponder
from validators import validate_meeting_schema
import simplejson


def get_meeting_by_id(meeting_id):
    meeting = Meeting()
    meeting.id = meeting_id
    meeting.get_meeting()
    return meeting


def user_auth(request):
    auth = Auth(auth_header=request.headers)
    return auth


class ApiMeeting(object):
    def __init__(self):
        pass

    def on_get(self, request, response, group_id, meeting_id=None):
        auth = user_auth(request)
        if meeting_id is not None:
            meeting = Meeting()
            meeting.id = meeting_id
            meeting.get_meeting()
            meeting_data = meeting.meeting_for_json(auth_key=auth.auth_key)
            response.data = MeetingResponder.respond(meeting_data,
                                                     linked={'groups': meeting_data['groups'],
                                                             'attendees': meeting_data['attendees']})
        else:  # get list of meetings order by date top 5
            pass
        response.content_type = 'application/json'
        response.status = falcon.HTTP_200

    def on_post(self, request, response, group_id):
        auth = user_auth(request)
        if auth.is_authorized_user:
            group = Group()
            group.id = group_id
            if group.allow_edit(auth_key=auth.auth_key):
                raw_json = request.stream.read()
                result_json = simplejson.loads(raw_json, encoding='utf-8')
                if validate_meeting_schema.validate_meeting(result_json):
                    meeting = Meeting()
                    meeting.set_meeting_properties(result_json['meeting'])
                    meeting.create_meeting(group_id=group_id)
                    response.content_type = 'application/json'
                    response.status = falcon.HTTP_201
                else:
                    response.status = falcon.HTTP_400
            else:
                response.status = falcon.HTTP_401
        else:
            response.status = falcon.HTTP_401


    def on_put(self, request, response, group_id, meeting_id):
        auth = user_auth(request)
        if auth.is_authorized_user:
            meeting = Meeting()
            meeting.id = meeting_id
            group = Group()
            group.id = group_id
            #TODO check against json schema -- when is best to do this?
            if group.allow_edit(auth_key=auth.auth_key):
                raw_json = request.stream.read()
                result_json = simplejson.loads(raw_json, encoding='utf-8')
                if validate_meeting_schema.validate_meeting(result_json):
                    meeting.set_meeting_properties(result_json['meeting'])
                    meeting.update_meeting()
                    response.content_type = 'application/json'
                    response.status = falcon.HTTP_201
                else:
                    response.status = falcon.HTTP_400
            else:
                response.status = falcon.HTTP_401
        else:
            response.status = falcon.HTTP_401


