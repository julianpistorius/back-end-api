__author__ = 'Marnee Dearman'
from agora_db.py2neo_group import AgoraGroup
from serializers import GroupResponder
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

    def on_get(self, request, response, group_id):
        #TODO get group interests
        pass

    def get_group_interests(self, group_id):
        pass


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