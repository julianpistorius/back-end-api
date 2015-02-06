__author__ = 'Marnee Dearman'
import falcon
# import os
# import images
import users, interests, locations, groups, organizations
#import interest

def crossdomain(req, resp):
    resp.set_header('Access-Control-Allow-Origin', '*')

def cors_middleware(request, response, params):
    response.set_header(
        'Access-Control-Allow-Origin',
        '*'
    )
    response.set_header(
        'Access-Control-Allow-Credentials',
        'true'
    )
    response.set_header(
        'Access-Control-Allow-Headers',
        'X-Auth-User, X-Auth-Key, Content-Type'
    )
    response.set_header(
        'Access-Control-Allow-Methods',
        'GET, PUT, POST, DELETE, OPTIONS'
    )


api = application = falcon.API(after=[crossdomain], before=[cors_middleware])

user_profile = users.UserProfile()
user_interests = users.UserInterests()
user = users.User()
user_goals = users.UserGoals()
user_interest_goals = users.UserInterestGoals()
local_shared_users = users.LocalUsersSharedInterests()
user_locations = users.UserLocations()
user_groups = users.UserGroups()
user_organizations = users.UserOrganizations()
interest = interests.Interest()
location = locations.Location()
location_interests = locations.LocationInterests()
location_users = locations.LocationUsers()
location_groups = locations.LocationGroups()
location_organizations = locations.LocationOrganizations()
group = groups.Group()
group_users = groups.GroupUsers()
group_interests = groups.GroupInterests()
group_goals = groups.GroupGoals()
group_achievements = groups.GroupAchievements()
organization = organizations.Organization()
org_users = organizations.OrganizationUsers()
org_interests = organizations.OrganizationInterests()


# api.add_route('/login/{token}')

#USER SPECIFIC
# api.add_route('/users/profile/{email}', user_profile)
#get all the stuff related to my user
api.add_route('/users/{email}', user)
api.add_route('/users/{email}/locations', user_locations)
api.add_route('/users/{email}/interests', user_interests)
api.add_route('/users/{email}/interests/{interest_id}', user_interests)
api.add_route('/users/{email}/interests/{interest_id}/goals', user_interest_goals)
api.add_route('/users/{email}/interests/{interest_id}/goals/{goal_id}', user_interest_goals)
api.add_route('/users/{email}/interests/{interest_id}/goals', user_interest_goals)
api.add_route('/users/{email}/interests', user_interests)

api.add_route('/users/{email}/goals/{goal_id}', user_goals)
api.add_route('/users/{email}/goals', user_goals)

#get general location view -- share interests, shared interest groups, shared organizations
#get stuff related to the location  (paged?)
api.add_route('/locations/{place_id}/interests', location_interests)
api.add_route('/locations/{place_id}/interests/{interest_id}/users', location_users)
api.add_route('/locations/{place_id}/interests/{interest_id}/groups', location_groups)
api.add_route('/locations/{place_id}/interests/{interest_id}/organizations', location_organizations)

api.add_route('/users/{email}/groups/{group_id}', user_groups)
api.add_route('/users/{email}/groups', user_groups)

api.add_route('/groups/{group_id}', group)
api.add_route('/groups/{group_id}/goals', group_goals)
api.add_route('/groups/{group_id}/achievements', group_achievements)
api.add_route('/groups/{group_id}/users', group_users)
api.add_route('/groups/{group_id}/interests', group_interests)

api.add_route('/organizations/{org_id}', organization)
api.add_route('/organizations/{org_id}/interests', org_interests)
api.add_route('/organizations/{org_id}/users', org_users)

#get users with shared interests with shared location
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




