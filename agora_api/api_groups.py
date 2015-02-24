import falcon
from agora_db.interest import AgoraInterest

__author__ = 'Marnee Dearman'
from agora_db.group import AgoraGroup
from api_serializers import GroupResponder
import simplejson

def get_group(group_id):
    agora_group = AgoraGroup()
    agora_group.id = group_id
    agora_group.get_group()
    return agora_group


class Group(object):
    def __init__(self):
        pass

    def on_get(self, request, response, group_id):
        #TODO get group details -- what should those be here?
        return self.get_group_json(group_id)

    def on_post(self, request, response):
        #TODO create group
        pass

    def on_put(self, requests, response):
        #TODO update group
        pass

    def get_group_json(self, group_id):
        group_details = get_group(group_id).group_for_json()
        json = GroupResponder.respond(group_details)
        return json


class GroupUsers(object):
    def __init__(self):
        pass

    def on_get(self, request, response, group_id):
        #TODO get groups members
        pass

    def get_group_members_json(self, group_id):
        pass


class GroupInterests(object):
    def __init__(self):
        pass

    def on_post(self, request, response, group_id):
        raw_json = request.stream.read()
        result_json = simplejson.loads(raw_json, encoding='utf-8')
        self.create_add_interests(result_json['interests'], group_id)
        response.status = falcon.HTTP_201
        response.body = simplejson.dumps(result_json, encoding='utf-8')

    # def on_get(self, request, response, group_id):
    #     response.data = self.get_group_interests_json(group_id)
    #     pass
    #
    # def get_group_interests_json(self, group_id):
    #     group = AgoraGroup()
    #     group.id = group_id
    #     group.get_group()
    #     return group.

    def create_add_interests(self, interests_json, group_id):
        group = AgoraGroup()
        group.id = group_id
        group.get_group()
        for interest_dict in interests_json:
            interest = AgoraInterest()
            interest.name = interest_dict['name']
            interest.description = interest_dict['description']
            interest.create_interest()
            # rel_properties = {}
            # rel_properties['experience'] = interest_dict['experience']
            # rel_properties['time'] = interest_dict['time']
            group.add_interest(interest.id)
        json = group.group_for_json()
        return json

class GroupAchievements(object):
    def __int__(self):
        pass

    def on_get(self, requests, response, group_id):
        #TODO get a sample of recent achievements from users
        pass

    def get_group_achievements_json(self, group_id):
        pass


class GroupGoals(object):
    def __init__(self):
        pass

    def on_get(self, requests, response, group_id):
        #TODO get a sample of recent goals from users
        pass

    def get_group_goals_json(self, group_id):
        pass