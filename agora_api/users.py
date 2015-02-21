__author__ = 'Marnee Dearman'
# import os
# import time
# import uuid
import sys
import falcon
from itsdangerous import BadSignature, BadTimeSignature
# import msgpack_pure
from agora_db.user import AgoraUser
from agora_db.interest import AgoraInterest
from agora_db.goal import AgoraGoal
from agora_db.location import AgoraLocation
from agora_db.group import AgoraGroup
from agora_db.organization import AgoraOrganization
from agora_db.achievement import AgoraAchievement

from serializers import UserResponder, \
    UserInterestResponder, UserGoalsResponder, UserLocationsResponder, \
    UserSharedInterestsResponder, UserProfileResponder, UserGroupsResponder, \
    GoalResponder, GroupResponder, ActivatedUserResponder
import simplejson
from marshmallow import Schema, fields

def get_user(email):
    agora_user = AgoraUser()
    agora_user.email = email
    agora_user.get_user()
    return agora_user

def get_goal(id):
    agora_goal = AgoraGoal()
    agora_goal.id = id
    agora_goal.get_goal()
    return agora_goal

def get_group(id):
    agora_group = AgoraGroup()
    agora_group.id = id
    agora_group.get_group()
    return agora_group

class User(object):
    def __init__(self):
        pass

    def on_get(self, request, response, email):
        response.data = self.get_user_json(email)
        response.content_type = 'application/json'
        response.status = falcon.HTTP_200

    def on_post(self, request, response, email=None):
        raw_json = request.stream.read()
        result_json = simplejson.loads(raw_json, encoding='utf-8')
        if email is None:
            self.register_user(result_json['user']['email'])
        else:
            self.update_user(result_json['user'])
        response.status = falcon.HTTP_201
        response.body = simplejson.dumps(result_json, encoding='utf-8')

    def on_put(self, request, response, email):
        raw_json = request.stream.read()
        result_json = simplejson.loads(raw_json, encoding='utf-8')
        # self.create_user(result_json['user'])
        self.update_user(result_json['user'])
        response.status = falcon.HTTP_201
        response.body = simplejson.dumps(result_json, encoding='utf-8')

    def get_user_json(self, email):
        user_data = get_user(email).user_relationships_for_json()
        json = UserResponder.respond(user_data, linked={'interests': user_data['interests'],
                                                        'groups': user_data['groups'],
                                                        'locations': user_data['locations'],
                                                        'goals': user_data['goals'],
                                                        'organizations': user_data['organizations']})
        return json

    def register_user(self, user_result_json):
        register = AgoraUser()
        email = user_result_json['email']
        register.register_user(email=email)

    def create_user(self, user_result_json):
        new_user = AgoraUser()
        new_user.set_user_properties(user_result_json)
        new_user.create_user()

    def update_user(self, user_result_json, email):
        user = AgoraUser()
        user.email = email
        user.get_user()
        user.set_user_properties(user_result_json)
        user.update_user()

class UserProfile(object):
    def __init__(self):
        pass

    def on_get(self, request, response, email):
        response.data = self.get_user_json(email)
        response.content_type = 'application/json'
        response.status = falcon.HTTP_200

    def on_post(self, request, response, email=None):
        raw_json = request.stream.read()
        result_json = simplejson.loads(raw_json, encoding='utf-8')
        self.create_user(result_json['user'])
        response.status = falcon.HTTP_201
        response.body = simplejson.dumps(result_json, encoding='utf-8')

    def on_put(self, request, response, email):
        raw_json = request.stream.read()
        result_json = simplejson.loads(raw_json, encoding='utf-8')
        self.update_user(result_json['user'])
        response.status = falcon.HTTP_202
        response.body = simplejson.dumps(result_json, encoding='utf-8')

    def get_user_json(self, email):
        """
        get agora user info and create dictionary for json response to client
        :return: simplejson
        """
        user_details = get_user(email).user_profile_for_json()
        json = UserProfileResponder.respond(user_details)
        return json
            # simplejson.dumps(get_user(email).user_details_for_json())

    def update_user(self, user_result_json):
        user = get_user(user_result_json['email'])
        user.set_user_properties(user_result_json)
        user.update_user()

    def create_user(self, user_result_json):
        #convert json to dictionary?
        new_user = AgoraUser()
        new_user.set_user_properties(user_result_json)
        new_user.create_user()
        # print new_user.name

class LocalUsersSharedInterests(object):
    def __init__(self):
        pass

    def on_get(self, request, response, email):
        response.data = self.get_shared_interests_user_json(email)
        response.content_type = 'application/json'
        response.status = falcon.HTTP_200

    def get_shared_interests_user_json(self, email):
        """
        get the local users with shared interests
        :param email:
        :return: json API
        """
        user_details = get_user(email).local_users_with_shared_interests_for_json()
        json = UserSharedInterestsResponder.respond(user_details, linked={'users': user_details['users']})
        return json

class UserInterests(object):
    def __init__(self):
        pass

    def on_get(self, request, response, email, interest_id=None):
        # if not interest_id is None:
        #     response.data = self.
        if interest_id is None:
            response.data = self.get_user_interests_json(email)
        else:
            #get details for user's interest -- goals, groups, organizations
            pass

        response.content_type = 'application/json'
        response.status = falcon.HTTP_200

    def on_post(self, request, response, email, interest_id=None):
        raw_json = request.stream.read()
        result_json = simplejson.loads(raw_json, encoding='utf-8')
        self.create_add_interests(result_json['interests'], email)
        response.status = falcon.HTTP_201
        response.body = simplejson.dumps(result_json, encoding='utf-8')

    def on_put(self, request, response, email):
        pass

    def get_user_interests_json(self, email):
        """

        :param email:
        :return: hyp json api format
        """
        user = get_user(email).user_interests_for_json()
        print user
        #TODO try doing this by building the interests separately -- probably dont need to do this
        response = UserInterestResponder.respond(user, linked={'interests': user['interests']})
        # .respond(user_interests)
        return response

    def create_add_interests(self, interests_json, email):
        #TODO create interests in batches not just singly
        user = get_user(email=email)
        for interest in interests_json:
            interest = AgoraInterest()
            # interest.set_interest_attributes(interest_json)
            interest.name = interests_json['name']
            interest.description = interests_json['description']
            interest.create_interest()
            rel_properties = {}
            rel_properties['experience'] = interests_json['experience']
            rel_properties['time'] = interests_json['time']
            user.add_interest(interest.id, rel_properties)
        json = user.user_interests_for_json()
        return json

    # def get_user_interest_goals_groups_organizations(self, interest_id):


class UserGoals(object):
    def __init__(self):
        pass

    def on_get(self, request, response, email): #@, goal_id=None):
        # if not goal_id is None:
        response.data = self.get_user_goals_json(email)
        # else:
        #     response.data = self.get_goal_json(goal_id)
        response.content_type = 'application/json'
        response.status = falcon.HTTP_200

    def on_post(self, request, response, email): #, goal_id=None):
        """
        create a goal
        :param request:
        :param response:
        :param email:
        :param goal_id:
        :return:
        """
        #TODO get goal interests, too
        raw_json = request.stream.read()
        result_json = simplejson.loads(raw_json, encoding='utf-8')
        self.create_goal(result_json['goal'], email)
        response.status = falcon.HTTP_201
        response.body = simplejson.dumps(result_json, encoding='utf-8')

    def on_put(self, request, response, email, goal_id=None):
        """
        update a goal
        :param request:
        :param response:
        :param email:
        :return:
        """
        raw_json = request.stream.read()
        result_json = simplejson.loads(raw_json, encoding='utf-8')
        goal = result_json['goal']

    def get_user_goals_json(self, email):
        user_goals = get_user(email).user_goals_for_json()

        json = UserGoalsResponder.respond(user_goals,
                                          linked={'goals': user_goals['goals']})
        return json

# response = UserInterestResponder.respond(user, linked={'interests': user['interests']})


    def create_goal(self, goal_json, email):
        user = get_user(email)
        user.get_user()
        goal = AgoraGoal()
        goal.set_goal_properties(goal_json)
        # goal.title = goal_json['title']
        # goal.description = goal_json['description']
        # goal.start_date = goal_json['start_date']
        # goal.end_date = goal_json['end_date']
        # goal.is_public = goal_json['is_public']
        # goal.achieved = goal_json['achieved']
        # goal.create_goal()
        # goal_interests = goal_json['interests']
        # for interest in goal_interests:
        #     goal.add_interest(interest['id'])
        # for key, value in goal_interests.iteritems():
        #     goal.add_interest()

class UserGroups(object):
    def __init__(self):
        pass

    def on_get(self, request, response, email, group_id=None):
        if not group_id is None:
            response.data = self.get_group_json(group_id)
        else:
            response.data = self.get_user_groups_json(email)
        response.content_type = 'application/json'
        response.status = falcon.HTTP_200

    def get_user_groups_json(self, email):
        user_groups = get_user(email).user_groups_for_json()
        json = UserGroupsResponder.respond(user_groups, linked={'groups': user_groups['groups']})
        return json

    def get_group_json(self, group_id):
        group = get_group(id).group_for_json()
        json = GroupResponder.respond(group, linked={'interests': group['interests'],
                                                    'users': group['users']})
        return json


class UserGroupAchievements(object):
    def __init__(self):
        pass

    def on_get(self, response, request, group_id):
        pass

class UserLocations(object):
    def __init__(self):
        pass

    def on_get(self, request, response, email, location_id=None):
        if not location_id is None:
            response.data = self.get_location_json(email, location_id)
        else:
            response.data = self.get_user_locations_json(email)
        response.content_type = 'application/json'
        response.status = falcon.HTTP_200

    def get_user_locations_json(self, email):
        user_locations = get_user(email).user_locations_for_json()
        json = UserLocationsResponder.respond(user_locations)
        return json

    def get_location_json(self, email, location_id):
        #TODO link in the related interests?
        pass


class UserOrganizations(object):
    def __int__(self):
        pass


class UserInterestGoals(object):
    def __init__(self):
        pass


class ActivateUser(object):
    def __init__(self):
        pass

    def on_post(self, request, response, payload):
        user = AgoraUser()
        response.content_type = 'application/json'
        raw_json = request.stream.read()
        result_json = simplejson.loads(raw_json, encoding='utf-8')
        user_json = result_json['user']
        email = user_json['email']
        try:
            user.activate_user(payload=payload, email=email)
            response.data = ActivatedUserResponder.respond(user.activated_user_for_json())   # UserProfileResponder.respond(user.user_profile_for_json())
            response.status = falcon.HTTP_201  #created
        except BadSignature as e:
            response.status = falcon.HTTP_400

# class RegisterUser(object):
#     def __init__(self):
#         pass
#
#     def on_post(self, request, response):
#         user = AgoraUser()
#         raw_json = request.stream.read()
#         result_json = simplejson.loads(raw_json, encoding='utf-8')
#         user.register_user(result_json['email'])
#         response.status = falcon.HTTP_202  # ok
