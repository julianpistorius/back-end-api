__author__ = 'Marnee Dearman'

import falcon
from db.interest import Interest
from db.group import Group
from db.auth import Auth
from base import ApiBase
from api_serializers import GroupResponder, SearchResponder
from validators.validate_group_schema import validate_group


class ApiGroup(ApiBase):
    def on_get(self, request, response, group_id=None):
        #TODO get group details
        self.authorize_user(request)
        if group_id is not None:
            response.data = self.get_group_json(group_id=group_id, auth_id=self.user_id)
        else:
            if len(request.params) > 0:
                match = request.params['match']
                limit = int(request.params['limit'])
                search_results = Group().matched_groups(match_string=match,
                                                             limit=limit)
                response.data = SearchResponder.respond(search_results,
                                                        linked={'groups': search_results['groups']})
        response.content_type = 'application/json'
        response.status = falcon.HTTP_200

    def on_post(self, request, response):
        if self.authorize_user(request):
            if self.validate_json(request, validate_group):
                self.create_group(self.result_json, auth_id=self.user_id)
                response.status = falcon.HTTP_201  # created
            else:
                response.status = falcon.HTTP_400
        else:
            response.status = falcon.HTTP_401

    def on_put(self, request, response):
        # #TODO update group
        # #TODO check if the user is a moderator or creator to update this group profile
        if self.authorize_user(request):
            if self.validate_json(request, validate_group):
                self.update_group(group_json=self.result_json, auth_id=self.user_id)
            else:
                response.status = falcon.HTTP_400
        else:
            response.status = falcon.HTTP_401

    def get_group_json(self, group_id, auth_id):
        group_details = self.get_group(group_id).group_for_json()
        json = GroupResponder.respond(group_details)
        return json

    def create_group(self, group_json, auth_id):
        group = Group()
        group.set_group_properties(group_json['group'])
        group.create_group()
        # TODO link to creator
        # TODO group location should default to the user's location(s)

    def update_group(self, group_json, auth_id):
        pass


class GroupMembers(object):
    def __init__(self):
        pass


class GroupInterests(ApiBase):
    def on_post(self, request, response, group_id):
        group = self.get_group(group_id=group_id)
        user = self.get_group_user(group.group_creator)
        if self.authorize_user(request) and user.id == self.user_id:
            if self.validate_json(request, validate_group):
                self.create_add_interests(self.result_json['interests'], group_id)
                response.status = falcon.HTTP_201
                #TODO user reponder?
                # response.body = simplejson.dumps(result_json, encoding='utf-8')
        else:
            response.status = falcon.HTTP_401

    # def on_get(self, request, response, group_id):
    #     response.data = self.get_group_interests_json(group_id)
    #     pass
    #
    # def get_group_interests_json(self, group_id):
    #     group = Group()
    #     group.id = group_id
    #     group.get_group()
    #     return group.

    def create_add_interests(self, interests_json, group_id):
        group = Group()
        group.id = group_id
        group.get_group()
        for interest_dict in interests_json:
            interest = Interest()
            interest.name = interest_dict['name']
            interest.description = interest_dict['description']
            interest.create_interest()
            # rel_properties = {}
            # rel_properties['experience'] = interest_dict['experience']
            # rel_properties['time'] = interest_dict['time']
            group.add_interest(interest.id)
        json = group.group_for_json()
        return json

class ApiGroupAchievements(object):
    def __int__(self):
        pass

    def on_get(self, requests, response, group_id):
        #TODO get a sample of recent achievements from users
        pass

    def get_group_achievements_json(self, group_id):
        pass


class ApiGroupGoals(object):
    def __init__(self):
        pass

    def on_get(self, requests, response, group_id):
        #TODO get a sample of recent goals from users
        pass

    def get_group_goals_json(self, group_id):
        pass