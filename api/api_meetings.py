__author__ = 'marnee'
import sys
import falcon
from db.meeting import Meeting
from db.group import Group
from api_serializers import MeetingResponder
from base import ApiBase
from validators.validate_meeting_schema import validate_meeting


class ApiMeeting(ApiBase):
    def on_get(self, request, response, group_id, meeting_id=None):
        # auth = user_auth(request)
        self.authorize_user(request)
        if meeting_id is not None:
            meeting = Meeting()
            meeting.id = meeting_id
            meeting.get_meeting()
            meeting_data = meeting.meeting_for_json(auth_key=self.user_id)
            response.data = MeetingResponder.respond(meeting_data,
                                                     linked={'groups': meeting_data['groups'],
                                                             'attendees': meeting_data['attendees']})
        else:  # get list of meetings order by date top 5
            pass
        response.content_type = 'application/json'
        response.status = falcon.HTTP_200

    def on_post(self, request, response, group_id):
        # auth = user_auth(request)
        if self.authorize_user(request):
            group = Group()
            group.id = group_id
            if group.allow_edit(auth_key=self.user_id):
                if self.validate_json(request, validate_meeting):
                    meeting = Meeting()
                    meeting.set_meeting_properties(self.result_json['meeting'])
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
        if self.authorize_user(request):
            meeting = Meeting()
            meeting.id = meeting_id
            group = Group()
            group.id = group_id
            #TODO check against json schema -- when is best to do this?
            if group.allow_edit(auth_key=self.user_id):
                if self.validate_json(request, validate_meeting):
                    meeting.set_meeting_properties(self.result_json['meeting'])
                    meeting.update_meeting()
                    response.content_type = 'application/json'
                    response.status = falcon.HTTP_201
                else:
                    response.status = falcon.HTTP_400
            else:
                response.status = falcon.HTTP_401
        else:
            response.status = falcon.HTTP_401


