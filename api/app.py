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
api.add_route('/activate/', activate)  # GET users api key (x-auth-key)
api.add_route('/users/', user)  # GET list of users by matching on name, POST to register user
api.add_route('/users/{user_id}', user)  # GET user information
api.add_route('/users/{user_id}/locations', user) # GET user locations, POST to add location, DELETE to remove location
api.add_route('/users/{user_id}/locations/{location_id}', user)  # GET connections for user's location
api.add_route('/users/{user_id}/interests', user)  # GET interests, POST to add new interest
api.add_route('/users/{user_id}/interests/{interest_id}', user)  # GET connections for interest, PUT to update interest

#TODO may not need this for now
# api.add_route('/users/{user_id}/interests/{interest_id}/goals', user_interest_goals)
# api.add_route('/users/{user_id}/interests/{interest_id}/goals/{goal_id}', user_interest_goals)
# api.add_route('/users/{user_id}/interests/{interest_id}/goals', user_interest_goals)

# USER COLLECTIONS
api.add_route('/users/{user_id}/goals/{goal_id}', user)  # PUT to update goa (achieved), DELETE to drop goal
api.add_route('/users/{user_id}/goals', user)  # GET to get list of goals
api.add_route('/users/{user_id}/conversations', user)  # GET to get list of conversations.  POST to start a conversation
api.add_route('/users/{user_id}/conversations/{conversation_id}', user)  # GET conversation and response.
# PUT to edit original conversation topic
api.add_route('/users/{user_id}/conversations/{conversation_id}/responses', user)  # POST a new response
api.add_route('/users/{user_id}/conversations/{conversation_id/responses/{response_id}', user)  # PUT update response.
# DELETE to drop response

# INTEREST COLLECTIONS
# api.add_route('/interests', interest)  # GET search by interest name
# api.add_route('/interests/{interest_id}', interest)  # GET return connections to the interest


# LOCATION COLLECTIONS
api.add_route('/locations/{place_id}/interests', location)  # GET search by interest name
# return interests connections for this location (users, groups, orgs)
api.add_route('/locations/{place_id}/interests/{interest_id}/users', location)  # GET search by user name
# return connections for this location
api.add_route('/locations/{place_id}/interests/{interest_id}/groups', location)  # GET search by group name
# return connections
api.add_route('/locations/{place_id}/interests/{interest_id}/organizations', location)  # GET search by org name
# return connections

# GROUPS COLLECTIONS
api.add_route('/groups', group)  # POST new group
api.add_route('/groups/{group_id}', group)  # GET group information and related data
api.add_route('/groups/{group_id}/goals', group)  # GET list of group goals.  POST to create new goal.
api.add_route('/groups/{group_id}/goals/{goal_id}', group)  # PUT to update goal.  DELETE to drop goal
api.add_route('/groups/{group_id}/members', group)  # GET list of group members
api.add_route('/groups/{group_id}/interests', group)  # GET list of interests.  POST to add new interest
api.add_route('/groups/{group_id}/meetings', group)  # GET list of meeting.  POST to add new meeting
api.add_route('/groups/{group_id}/meetings/{meeting_id}', group)  # GET meeting details.  PUT to update meeting
api.add_route('/groups/{group_id}/conversations/', group)  # GET list of conversations.  POST to create new conversation
api.add_route('/groups/{group_id}/conversations/{conversation_id}', group)  # GET conversation.
# PUT to update conversation.  DELETE to drop conversation
api.add_route('/groups/{group_id}/conversations/{conversation_id}/responses', group)  # GET responses.
# POST to add a response.
api.add_route('/groups/{group_id}/conversations/{conversation_id}/responses/{response_id}', group)
# PUT to edit response  DELETE to drop response

# ORGANIZATION COLLECTIONS
api.add_route('/organizations', organization)  # POST to create an organization
api.add_route('/organizations/{org_id}', organization)  # GET all the stuff related to this org
api.add_route('/organizations/{org_id}/interests', organization)  # GET list of interests  POST new interest
api.add_route('/organizations/{org_id}/interests/{interest_id}', organization)  # GET interest.  PUT to update
# DELETE to drop interest
api.add_route('/organizations/{org_id}/members', organization)  # GET list of members
api.add_route('/organizations/{org_id}/goals/', organization)  # GET lis of goals POST new goal
api.add_route('/organizations/{org_id}/goals/{goal_id}', organization)  # GET goal PUT update to goal DELETE drop goal
api.add_route('/organizations/{org_id}/meetings', organization)  # GET list of meeting and POST new meeting
api.add_route('/organizations/{org_id}/meetings/{meeting_id}', organization)  # PUT to update meeting





