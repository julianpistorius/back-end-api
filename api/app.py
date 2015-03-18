__author__ = 'Marnee Dearman'

from api import api_conversations

import falcon
# import os
# import images
import api_users, api_interests, api_locations, api_groups, api_organizations, api_meetings
#import interest

def crossdomain(req, resp):
    resp.set_header('Access-Control-Allow-Origin', '*')

def cors_middleware(request, response, params):
    response.set_header(
        'Access-Control-Allow-Origin',
        '*'
    )
    # response.set_header(
    #     'Access-Control-Allow-Credentials',
    #     'true'
    # )
    response.set_header(
        'Access-Control-Allow-Headers',
        'X-Auth-User, X-Auth-Key, Content-Type'
    )
    response.set_header(
        'Access-Control-Allow-Methods',
        'GET, PUT, POST, PATCH, DELETE, OPTIONS'
    )


api = application = falcon.API(after=[crossdomain], before=[cors_middleware])

user = api_users.ApiUser()
group = api_groups.ApiGroup()
organization = api_organizations.ApiOrganization()
interest = api_interests.ApiInterest()
location = api_locations.ApiLocation()
# conversation = api_conversations.ApiConversation()
# meeting = api_meetings.Meeting()
activate = api_users.ApiActivateUser()

# USER COLLECTIONS
# this will activate a user account
api.add_route('/activate/', activate)
api.add_route('/users/', user)
api.add_route('/users/{user_id}', user)
api.add_route('/users/{user_id}/locations', user)
api.add_route('/users/{user_id}/locations/{location_id}', user)
api.add_route('/users/{user_id}/interests', user)
api.add_route('/users/{user_id}/interests/{interest_id}', user)

#TODO may not need this for now
# api.add_route('/users/{user_id}/interests/{interest_id}/goals', user_interest_goals)
# api.add_route('/users/{user_id}/interests/{interest_id}/goals/{goal_id}', user_interest_goals)
# api.add_route('/users/{user_id}/interests/{interest_id}/goals', user_interest_goals)

# USER COLLECTIONS
api.add_route('/users/{user_id}/goals/{goal_id}', user)
api.add_route('/users/{user_id}/goals', user)
api.add_route('/users/{user_id}/conversations', user)
api.add_route('/users/{user_id}/conversations/{conversation_id}', user)
api.add_route('/users/{user_id}/conversations/{conversation_id}/responses', user)
api.add_route('/users/{user_id}/conversations/{conversation_id/responses/{response_id}', user)

# INTEREST COLLECTIONS
api.add_route('/interests', interest)  # GET search by interest name
api.add_route('/interests/{interest_id}', interest)  # GET return relationships to the interest in the user's location(s)


# LOCATION COLLECTIONS
api.add_route('/locations/{place_id}/interests', location)
api.add_route('/locations/{place_id}/interests/{interest_id}/users', location)
api.add_route('/locations/{place_id}/interests/{interest_id}/groups', location)
api.add_route('/locations/{place_id}/interests/{interest_id}/organizations', location)

# GROUPS COLLECTIONS
api.add_route('/groups/', group)
api.add_route('/groups/{group_id}', group)
api.add_route('/groups/{group_id}/goals', group)
api.add_route('/groups/{group_id}/goals/{goal_id}', group)
api.add_route('/groups/{group_id}/members', group)
api.add_route('/groups/{group_id}/interests', group)
api.add_route('/groups/{group_id}/meetings', group)  # GET and POST
api.add_route('/groups/{group_id}/meetings/{meeting_id}', group)  # PUT
api.add_route('/groups/{group_id}/conversations/', group)
api.add_route('/groups/{group_id}/conversations/{conversation_id}', group)

# ORGANIZATION COLLECTIONS
api.add_route('/organizations/{org_id}', organization)  #GET all the stuff related to this org
api.add_route('/organizations/{org_id}/interests', organization)  #GET list of interests  POST new interests, DELETE interest
api.add_route('/organizations/{org_id}/users', organization)  #GET list of members DELETE members
api.add_route('/organizations/{org_id}/goals/', organization)  #GET lis of goals POST new goal
api.add_route('/organizations/{org_id}/goals/{goal_id}', organization)  #GET goal PUT update to goal
api.add_route('/organizations/{org_id}/meetings', organization)  # GET and POST
api.add_route('/organizations/{org_id}/meetings/{meeting_id}', organization)  # PUT





