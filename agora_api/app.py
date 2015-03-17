__author__ = 'Marnee Dearman'
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

user = api_users.User()
user_locations = api_users.UserLocations()

user_interests = api_users.UserInterests()
user_goals = api_users.UserGoals()
user_interest_goals = api_users.UserInterestGoals()
local_shared_users = api_users.LocalUsersSharedInterests()
user_groups = api_users.UserGroups()
user_organizations = api_users.UserOrganizations()
interests = api_interests.Interest()
location = api_locations.Location()
location_interests = api_locations.LocationInterests()
location_users = api_locations.LocationUsers()
location_groups = api_locations.LocationGroups()
location_organizations = api_locations.LocationOrganizations()
groups = api_groups.Group()
# group_users = api_groups.GroupUsers()
group_interests = api_groups.GroupInterests()
group_goals = api_groups.GroupGoals()
group_achievements = api_groups.GroupAchievements()
organization = api_organizations.Organization()
org_users = api_organizations.OrganizationUsers()
org_interests = api_organizations.OrganizationInterests()

meetings = api_meetings.Meeting()

activate = api_users.ActivateUser()
# register = users.RegisterUser()

# api.add_route('/login/{token}')

# USER COLLECTIONS

# this will create a user account if it does not exist
api.add_route('/activate/', activate)

# use this route to register/login users
#GET users based on query string field=''
api.add_route('/users/', user)
# GET and POST user data
api.add_route('/users/{user_id}', user)

# USER LOCATIONS
api.add_route('/users/{user_id}/locations', user_locations)
api.add_route('/users/{user_id}/locations/{location_id}', user_locations)

# USER INTERESTS
api.add_route('/users/{user_id}/interests', user_interests)
# GET a list of interests for the user
api.add_route('/users/{user_id}/interests/{interest_id}', user_interests)
# GET a view of the
api.add_route('/users/{user_id}/interests/{interest_id}/goals', user_interest_goals)
api.add_route('/users/{user_id}/interests/{interest_id}/goals/{goal_id}', user_interest_goals)
api.add_route('/users/{user_id}/interests/{interest_id}/goals', user_interest_goals)

# USER GOALS
api.add_route('/users/{user_id}/goals/{goal_id}', user_goals)
api.add_route('/users/{user_id}/goals', user_goals)

# USER GROUPS
api.add_route('/users/{user_id}/groups/{group_id}', user_groups)
api.add_route('/users/{user_id}/groups', user_groups)

#INTERESTS
api.add_route('/interests', interests)
api.add_route('/interests/{interest_id}', interests)

# get general location view -- share interests, shared interest groups, shared organizations
# get stuff related to the location  (paged?)

# LOCATION COLLECTIONS
api.add_route('/locations/{place_id}/interests', location_interests)
api.add_route('/locations/{place_id}/interests/{interest_id}/users', location_users)
api.add_route('/locations/{place_id}/interests/{interest_id}/groups', location_groups)
api.add_route('/locations/{place_id}/interests/{interest_id}/organizations', location_organizations)

# GROUPS COLLECTIONS
api.add_route('/groups/', groups)
api.add_route('/groups/{group_id}', groups)
api.add_route('/groups/{group_id}/goals', group_goals)
api.add_route('/groups/{group_id}/achievements', group_achievements)
api.add_route('/groups/{group_id}/users', group_users)
api.add_route('/groups/{group_id}/interests', group_interests)
# api.add_route('/groups/{group_id}/meetings', meetings)

# GROUP MEETINGS COLLECTIONS
api.add_route('/groups/{group_id}/meetings', meetings)  # GET and POST
api.add_route('/groups/{group_id}/meetings/{meeting_id}', meetings)  # PUT


# ORGANIZATION COLLECTIONS

api.add_route('/organizations/{org_id}', organization)
api.add_route('/organizations/{org_id}/interests', org_interests)
api.add_route('/organizations/{org_id}/users', org_users)

# ORG MEETINGS COLLECTIONS
api.add_route('/organizations/{org_id}/meetings', meetings)  # GET and POST
api.add_route('/organizations/{org_id}/meetings/{meeting_id}', meetings)  # PUT



# MEETING COLLECTIONS
# api.add_route('/meetings/{meeting_id}', meetings)  #get meeting details, put update to meeting
# api.add_route('/meetings/', meetings)  #post new meeting

# get users with shared interests with shared location
# api.add_route('/locations/{place_id}/interests/{interest_id}/users', )

# api.add_route('/interests/{interest_id}', interest)
# api.add_route('/interests/{interest_id}/locations/{place_id}/organizations', user_organizations)
# api.add_route('/interests/{interest_id}/locations/{place_id}/groups', )

# api.add_route('/locations/interests', location)

# api.add_route('/users/{email}/locations/{place_id}', user_locations)
# api.add_route('/users/{email}/locations/{place_id}/interests', user_interests)
# api.add_route('/users/{email}/locations/{place_id}/groups', user_groups)
# api.add_route('/users/{email}/locations/{place_id}/organizations', user_organizations)
# api.add_route('/users/{email}/locations', user_locations)




