from db.conversation import Conversation
from misc.decorators_experiments.authorization_decorator_class import AuthDecorator
from validators.decorators.json_validator_decorator import validate_request_json

__author__ = 'Marnee Dearman'
import sys
import falcon
from itsdangerous import BadSignature, BadTimeSignature
from db.auth import Auth
from db.user import User
from db.interest import Interest
from db.goal import Goal
from validators import validate_user_schema, validate_location_schema, validate_interest_schema
from validators import validate_goals_schema, validate_conversation_response_schema

from api_serializers import UserResponder, LocationResponder, OrganizationResponder,\
    GoalResponder, GroupResponder, ActivatedUserResponder, SearchResponder, ConversationResponder
import simplejson


def get_user_by_email(email):
    agora_user = User()
    agora_user.email = email
    agora_user.get_user()
    return agora_user


def get_user_by_id(user_id):
    agora_user = User()
    agora_user.id = user_id
    agora_user.get_user()
    return agora_user


def user_auth(request):
    auth = Auth(auth_header=request.headers)
    return auth


class ApiUser(object):
    def __init__(self):
        pass

# api.add_route('/users/', user)
# GET list of users by matching on name,
# POST to register user
# api.add_route('/users/{user_id}', user)
# GET user information
#     @AuthDecorator
    def on_get(self, request, response, user_id=None, **kwargs):  # , auth_key=None):
        auth = user_auth(request)
        if user_id is not None:  # get the specified user
            # response.data = self.get_user_responder(user_id=user_id, auth_id=self.auth_key)
            response.data = self.get_user_responder(user_id=user_id, auth_id=auth.auth_key)
            # response.data = self.get_user_responder(user_id=user_id, auth_id=auth_key)
        else:  # find by name return a list
            match = request.params['match']
            limit = int(request.params['limit'])
            search_results = User().matched_users(match_string=match, limit=limit)
            response.data = SearchResponder.respond(search_results,
                                                    linked={'users': search_results['users']})
        response.content_type = 'application/json'
        response.status = falcon.HTTP_200

    #TODO user a decorator to check authorization??
    #TODO use a decorator to check request object??
    # @AuthDecorator
    # @validate_request_json('register')
    def on_post(self, request, response):  #, **kwargs=None):
        raw_json = request.stream.read()
        result_json = simplejson.loads(raw_json, encoding='utf-8')
        # REGISTER USER -- does not create a user
        if validate_user_schema.validate_activate_user(result_json):
            self.register_user(result_json['user'])
            response.status = falcon.HTTP_200
        else:
            response.status = falcon.HTTP_400

    # @validate_request_json('register')
    def on_put(self, request, response, user_id):  # , **kwargs):
        auth = user_auth(request.auth)
        if auth.is_authorized_user and user_id == auth.auth_key:
            raw_json = request.stream.read()
            result_json = simplejson.loads(raw_json, encoding='utf-8')
            if validate_user_schema.validate_user(result_json):
                self.update_user(user_result_json=result_json['user'], user_id=user_id)
                response.status = falcon.HTTP_200
                # response.content_type = 'application/json'
                # response.body = simplejson.dumps(result_json, encoding='utf-8')
            else:
                response.status = falcon.HTTP_400
        else:
            response.status = falcon.HTTP_401  # unauthorized

    def get_user_responder(self, user_id, auth_id):
        user_data = get_user_by_id(user_id=user_id).user_relationships_for_json(auth_id=auth_id)
        json = UserResponder.respond(user_data, linked={'interests': user_data['interests'],
                                                        'groups': user_data['groups'],
                                                        'locations': user_data['locations'],
                                                        'goals': user_data['goals'],
                                                        'organizations': user_data['organizations']})
        return json

    def register_user(self, user_result_json):
        register = User()
        email = user_result_json['email']
        register.register_user(email=email)

    def update_user(self, user_result_json, user_id):
        user = User()
        user.id = user_id
        user.set_user_properties(user_result_json)
        user.update_user()


class ApiUserInterests(object):
    def __init__(self):
        pass
# api.add_route('/users/{user_id}/interests', user)
# GET list of interests,
# POST to add new interest
# api.add_route('/users/{user_id}/interests/{interest_id}', user)
# GET connections/recommendations for interest,
# PUT to update interest
# DELETE to drop interest

    def on_get(self, request, response, user_id, interest_id=None):
        auth = user_auth(request.headers)
        if auth.is_authorized_user:
            if interest_id is None:
                response.data = self.get_user_interests_responder(user_id)
            else:  # GET connections/recommendations for interest
                pass
            response.content_type = 'application/json'
            response.status = falcon.HTTP_200

        else:
            response.status = falcon.HTTP_401

    def on_post(self, request, response, user_id, interest_id=None):
        auth = user_auth(request.headers)
        if auth.is_authorized_user and auth.auth_key == user_id:
            raw_json = request.stream.read()
            result_json = simplejson.loads(raw_json, encoding='utf-8')
            if validate_interest_schema.validate_interest(result_json):
                self.add_interests(result_json['interest'], user_id=user_id)
                response.status = falcon.HTTP_201
                response.content_type = 'application/json'
                response.body = self.get_user_interests_responder(user_id)  # simplejson.dumps(result_json, encoding='utf-8')
            else:
                response.status = falcon.HTTP_400
        else:
            response.status = falcon.HTTP_401

    def on_put(self, request, response, user_id, interest_id):
        auth = user_auth(request)
        if auth.is_authorized_user and auth.auth_key == user_id:
            raw_json = request.stream.read()
            result_json = simplejson.loads(raw_json, encoding='utf-8')
            if validate_interest_schema.validate_interest(result_json):
                self.update_interest(user_id, interest_id, result_json['interest'])
                response.status = falcon.HTTP_200
                response.content_type = 'application/json'
                response.body = self.get_user_interests_responder(user_id)
            else:
                response.status = falcon.HTTP_400
        else:
            response.status = falcon.HTTP_401

    def on_delete(self, request, response, user_id, interest_id):
        auth = user_auth(request)
        if auth.is_authorized_user and auth.auth_key == user_id:
            self.delete_interest(user_id=user_id, interest_id=interest_id)
            response.body = self.get_user_interests_responder(user_id)
            response.status = falcon.HTTP_200
        else:
            response.status = falcon.HTTP_401

    def get_user_interests_responder(self, user_id):
        """

        :param user_id:
        :return: UserResponder
        """
        user = get_user_by_id(user_id).user_interests_for_json()
        response = UserResponder.respond(user, linked={'interests': user['interests']})
        return response

    def add_interests(self, interests_json, user_id):
        #TODO ??create interests in batches not just singly??
        user = get_user_by_id(user_id=user_id)
        for interest_dict in interests_json:
            interest = Interest()
            # interest.set_interest_attributes(interest_json)
            # interest.name = interest_dict['name']
            # interest.description = interest_dict['description']
            # interest.create_interest()
            rel_properties = {}
            rel_properties['experience'] = interest_dict['experience']
            rel_properties['time'] = interest_dict['time']
            user.add_interest(interest.id, rel_properties)

    def update_interest(self, user_id, interest_id, interest_rel_properties):
        user = get_user_by_id(user_id)
        experience_properties_dict = {}
        experience_properties_dict['experience'] = interest_rel_properties['experience']
        experience_properties_dict['time'] = interest_rel_properties['time']
        user.update_interest(interest_id=interest_id, experience_properties_dict=experience_properties_dict)

    def delete_interest(self, user_id, interest_id):
        user = get_user_by_id(user_id)
        user.delete_interest(interest_id=interest_id)


class ApiUserGoals(object):
    def __init__(self):
        pass

# api.add_route('/users/{user_id}/goals/{goal_id}', user)
# GET goal to update or delete
# PUT to update goa (achieved),
# DELETE to drop goal
# api.add_route('/users/{user_id}/goals', user)
# GET to get list of goals
# POST to add a new goal

    def on_get(self, request, response, user_id, goal_id=None):
        """

        :param request:
        :param response:
        :param user_id:
        :param goal_id:
        :return:
        """
        auth = user_auth(request)
        if goal_id is None:
            response.data = self.get_user_responder(user_id=user_id, auth_id=auth.auth_key)
            response.content_type = 'application/json'
            response.status = falcon.HTTP_200
        else:  # GET the goal details for view or edit
            response.data = self.get_goal_responder(user_id=user_id, goal_id=goal_id, auth_id=auth.auth_key)
            response.content_type = 'application/json'
            response.status = falcon.HTTP_200

    def on_post(self, request, response, user_id, goal_id=None):
        """
        create a goal
        :param request:
        :param response:
        :param user_id:
        :param goal_id:
        :return:
        """
        auth = user_auth(request)
        if auth.is_authorized_user and user_id == auth.auth_key:
            raw_json = request.stream.read()
            result_json = simplejson.loads(raw_json, encoding='utf-8')
            if validate_goals_schema.validate_goal(result_json):
                self.create_goal(result_json['goal'], user_id)
                response.status = falcon.HTTP_201
                response.body = self.get_user_responder(user_id, auth.auth_key)
                response.content_type = 'application/json'
            else:
                response.status = falcon.HTTP_400
        else:
            response.status = falcon.HTTP_401

    def on_put(self, request, response, user_id, goal_id):
        """
        update a goal
        :param request:
        :param response:
        :param user_id:
        :param goal_id:
        :return:
        """
        auth = user_auth(request)
        if auth.is_authorized_user and user_id == auth.auth_key:
            raw_json = request.stream.read()
            result_json = simplejson.loads(raw_json, encoding='utf-8')
            if validate_goals_schema.validate_goal(result_json):
                self.update_goal(goal_id, result_json['goal'])
                response.data = self.get_goal_responder(user_id, goal_id, auth.auth_key)
                response.content_type = 'application/json'
                response.status = falcon.HTTP_200
            else:
                response.status = falcon.HTTP_400
        else:
            response.status = falcon.HTTP_401

    def get_user_responder(self, user_id, auth_id):
        user_data = get_user_by_id(user_id=user_id).user_relationships_for_json(auth_id=auth_id)
        json = UserResponder.respond(user_data, linked={'goals': user_data['goals']})
        return json

    def create_goal(self, goal_json, user_id):
        user = get_user_by_id(user_id)
        user.add_goal(goal_json)

    def get_goal_responder(self, user_id, goal_id, auth_id):
        goal = Goal()
        goal.id = goal_id
        goal_data = goal.goal_for_json()
        goal_data['allow_edit'] = (user_id == auth_id)
        json = GoalResponder.respond(goal_data)
        return json

    def update_goal(self, goal_id, goal_properties):
        goal = Goal()
        goal.id = goal_id
        goal.set_goal_properties(goal_properties)
        goal.update_goal()


class ApiUserLocations(object):
    def __init__(self):
        pass
# api.add_route('/users/{user_id}/locations', user)
# GET user locations,
# POST to add location,
# api.add_route('/users/{user_id}/locations/{location_id}', user)
# GET connections/recommendations for user's location
# DELETE to remove location

    def on_get(self, request, response, user_id, location_id=None):
        auth = user_auth(request)
        if location_id is None:  # GET list of locations for view or edit
            response.data = self.get_user_responder(user_id=user_id, auth_id=auth.auth_key)
            response.content_type = 'application/json'
            response.status = falcon.HTTP_200
        else:  # GET connections or recommendations for location
            pass  #TODO recommendations and connections

    def on_post(self, request, response, user_id):
        auth = user_auth(request)
        raw_json = request.stream.read()
        result_json = simplejson.loads(raw_json, encoding='utf-8')
        if auth.is_authorized_user and auth.auth_key == user_id:
            if validate_location_schema.validate_location(result_json):
                user = get_user_by_id(user_id)
                user.add_location(result_json['location'])
                response.data = self.get_user_responder(user_id=user_id, auth_id=auth.auth_key)
                response.content_type = 'application/json'
                response.status = falcon.HTTP_201
            else:
                response.status = falcon.HTTP_400
        else:
            response.status = falcon.HTTP_401

    def on_delete(self, request, response, user_id, location_id):
        auth = user_auth(request)
        if auth.is_authorized_user and user_id == auth.auth_key:  # fulfill request
            user = get_user_by_id(user_id)
            pass  #TODO drop location

    def get_user_responder(self, user_id, auth_id):
        user_data = get_user_by_id(user_id=user_id).user_relationships_for_json(auth_id=auth_id)
        json = UserResponder.respond(user_data, linked={'locations': user_data['locations']})
        return json


class ApiUserConversations(object):
    def __init__(self):
        pass

# api.add_route('/users/{user_id}/conversations', user)  #
# GET to get list of conversations.
# POST to start a conversation
# api.add_route('/users/{user_id}/conversations/{conversation_id}', user)  #
# GET conversation and response.
# # PUT to edit original conversation topic
# api.add_route('/users/{user_id}/conversations/{conversation_id}/responses', user)  #
# POST a new response
# api.add_route('/users/{user_id}/conversations/{conversation_id/responses/{response_id}', user)  #
# PUT update response.
# DELETE to drop response

    def on_get(self, request, response, user_id, conversation_id=None):
        auth = user_auth(request)
        if conversation_id is None:  # GET list of conversations
            response.data = self.get_user_responder(user_id, auth.auth_key)
            response.content_type = 'application/json'
            response.status = falcon.HTTP_200
        else:  # GET specific conversation
            response.data = self.get_conversation_responder(user_id, conversation_id, auth.auth_key)
            response.content_type = 'application/json'
            response.status = falcon.HTTP_200

    def on_post(self, request, response, user_id):
        auth = user_auth(request)
        if auth.is_authorized_user and auth.auth_key != user_id:  # start conversation with user
            user = get_user_by_id(user_id)
            raw_json = request.stream.read()
            result_json = simplejson.loads(raw_json, encoding='utf-8')
            if validate_conversation_response_schema.validate_conversation(result_json):
                convo_id = user.create_converation_between_users(user_id_started=auth.auth_key,
                                                                 user_id_with=user_id,
                                                                 conversation_properties=result_json['conversation'])
                response.data = self.get_conversation_responder(user_id=user_id,
                                                                conversation_id=convo_id,
                                                                auth_id=auth.auth_key)
                response.status = falcon.HTTP_201
                response.content_type = 'application/json'
            else:
                response.status = falcon.HTTP_400
        else:
            response.status = falcon.HTTP_401

    def on_put(self, request, response, user_id, conversation_id):
        auth = user_auth(request)
        if auth.is_authorized_user:
            raw_json = request.stream.read()
            result_json = simplejson.loads(raw_json, encoding='utf-8')
            if validate_conversation_response_schema.validate_conversation(result_json):
                convo = Conversation()
                convo.id = conversation_id
                started_by_id = convo.started_by['id']
                if auth.auth_key == started_by_id:  # allow update
                    convo.set_conversation_properties(result_json['conversation'])
                    convo.update_conversation()
                    response.data = self.get_conversation_responder(user_id=user_id,
                                                                    conversation_id=conversation_id,
                                                                    auth_id=auth.auth_key)
                    response.content_type = 'application/json'
                    response.status = falcon.HTTP_200
                else:
                    response.status = falcon.HTTP_401
            else:
                response.status = falcon.HTTP_400
        else:
            response.status = falcon.HTTP_401

    def get_user_responder(self, user_id, auth_id):
        user_data = get_user_by_id(user_id).user_relationships_for_json(auth_id=auth_id)
        json = UserResponder.respond(user_data, linked={'conversations': user_data['conversations']})
        return json

    def get_conversation_responder(self, user_id, conversation_id, auth_id):
        conversation = Conversation()
        conversation.id = conversation_id
        convo_data = conversation.conversation_for_json()
        return ConversationResponder.respond(convo_data, linked={'users': convo_data['users'],
                                                                 'responses': convo_data['responses']})


class ApiActivateUser(object):
    def __init__(self):
        pass

    def on_post(self, request, response):
        user = User()
        response.content_type = 'application/json'
        raw_json = request.stream.read()
        result_json = simplejson.loads(raw_json, encoding='utf-8')
        if validate_user_schema.validate_activate_user(result_json):
            user_json = result_json['user']
            email = user_json['email']
            payload = user_json['payload']
            try:
                user.activate_user(payload=payload, email=email)
                response.data = ActivatedUserResponder.respond(user.activated_user_for_json())
                # UserProfileResponder.respond(user.user_profile_for_json())
                response.status = falcon.HTTP_201  #created
            except BadSignature as e:
                response.status = falcon.HTTP_400
        else:
            response.status = falcon.HTTP_400



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
        user_details = get_user_by_email(email).local_users_with_shared_interests_for_json()
        json = UserResponder.respond(user_details, linked={'users': user_details['users']})
        return json


# class ApiUserGroups(object):
#     def __init__(self):
#         pass
#
#     def on_get(self, request, response, user_id, group_id=None):
#         auth = user_auth(request.headers)
#         if auth.is_authorized_user and auth.auth_key == user_id:
#             if group_id is not None:
#                 response.data = self.get_group_json(group_id)
#             else:
#                 response.data = self.get_user_groups_json(user_id)
#             response.content_type = 'application/json'
#             response.status = falcon.HTTP_200
#
#     def on_post(self, request, response, user_id, group_id=None):
#         # user will join group
#         auth = user_auth(request.headers)
#         if auth.is_authorized_user and auth.auth_key == user_id:
#             user = get_user_by_id(user_id=user_id)
#             user.join_group(group_id=group_id)
#             response.status = falcon.HTTP_201
#             response.body = self.get_group_json(group_id=group_id)
#         else:
#             response.status = falcon.HTTP_401
#
#     def get_user_groups_json(self, user_id):
#         user_groups = get_user_by_id(user_id).user_groups_for_json()
#         json = UserResponder.respond(user_groups, linked={'groups': user_groups['groups']})
#         return json
#
#     def get_group_json(self, group_id):
#         group = get_group(id).group_for_json()
#         json = GroupResponder.respond(group, linked={'interests': group['interests'],
#                                                     'users': group['users']})
#         return json
#

# class RegisterUser(object):
#     def __init__(self):
#         pass
#
#     def on_post(self, request, response):
#         user = User()
#         raw_json = request.stream.read()
#         result_json = simplejson.loads(raw_json, encoding='utf-8')
#         user.register_user(result_json['email'])
#         response.status = falcon.HTTP_202  # ok
