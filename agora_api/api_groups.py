import falcon
from agora_db.interest import AgoraInterest
from agora_db.user import AgoraUser

__author__ = 'Marnee Dearman'
from agora_db.group import AgoraGroup
from agora_db.auth import Auth
from api_serializers import GroupResponder, SearchResponder
import simplejson


def get_group(group_id):
    agora_group = AgoraGroup()
    agora_group.id = group_id
    agora_group.get_group()
    return agora_group


def get_group_user(user_id):
    user = AgoraUser()
    user.id = user_id
    user.get_user()
    return user


def user_auth(request):
    auth = Auth(auth_header=request.headers)
    return auth


class Group(object):
    def __init__(self):
        pass

    def on_get(self, request, response, group_id=None):
        #TODO get group details
        auth = user_auth(request)
        if group_id is not None:
            pass
        else:
            match = request.params['match']
            limit = int(request.params['limit'])
            search_results = AgoraGroup().matched_groups(match_string=match,
                                                         limit=limit)
            response.data = SearchResponder.respond(search_results,
                                                    linked={'groups': search_results['groups']})
        response.content_type = 'application/json'
        response.status = falcon.HTTP_200


    def on_post(self, request, response):
        #TODO create group
        #TODO check against json schema -- when is best to do this?
        pass

    def on_put(self, requests, response):
        #TODO update group
        #TODO check against json schema -- when is best to do this?
        pass

    def get_group_json(self, group_id):
        group_details = get_group(group_id).group_for_json()
        json = GroupResponder.respond(group_details)
        return json

class GroupInterests(object):
    def __init__(self):
        pass

    def on_post(self, request, response, group_id):
        auth = user_auth(request.headers)
        group = get_group(group_id=group_id)
        user = get_group_user(group.creator)
        if auth.is_authorized_user and auth.auth_key == user.id:
            raw_json = request.stream.read()
            result_json = simplejson.loads(raw_json, encoding='utf-8')
            self.create_add_interests(result_json['interests'], group_id)
            response.status = falcon.HTTP_201
            response.body = simplejson.dumps(result_json, encoding='utf-8')
        else:
            response.status = falcon.HTTP_401

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