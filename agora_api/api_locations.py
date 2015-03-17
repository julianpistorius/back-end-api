__author__ = 'Marnee Dearman'
from agora_db.location import AgoraLocation
import simplejson
import falcon
from validators import validate_location_schema

#TODO locations come from Google maps api
# def get_location(name=None, postal_code=None, place_id=None):
#     #TODO return location by name or postal code
#     if not name is None:
#         return 'loc'
#     elif not postal_code is None:
#         return 'loc'
#     elif not place_id is None:
#         agora_location = AgoraLocation()
#         agora_location.id = place_id
#         agora_location.get_location()
#         return agora_location

#TODO check user authorization

class Location(object):
    def __init__(self):
        pass

    def on_get(self, response, request, place_id):
        #TODO return activity for location
        pass

    def on_post(self, request, response, user_id=None, group_id=None, organization_id=None):
        #TODO add location to user or group or organization
        raw_json = request.stream.read()
        result_json = simplejson.loads(raw_json, encoding='utf-8')
        if validate_location_schema.validate_location(result_json):
            pass  # handle adding location to entity
        else:
            response.status = falcon.HTTP_400

    def on_put(self, request, response, user_id=None, group_id=None, organization_id=None):
        #TODO change location
        raw_json = request.stream.read()
        result_json = simplejson.loads(raw_json, encoding='utf-8')
        if validate_location_schema.validate_location(result_json):
            pass
        else:
            response.status = falcon.HTTP_400

    # def on_delete(self, request, response, user_id=None, group_id=None, organization_id=None):
    #     #TODO remove location -- do

# class LocationInterests(object):
#     def __init__(self):
#         pass
#
#     def on_get(self, requests, response, place_id):
#         #TODO get location interests
#         pass
#
#     def get_location_interests_json(self, place_id):
#         location = get_location(place_id=place_id)
#
#
# class LocationUsers(object):
#     def __init__(self):
#         pass
#
#     def on_get(self, request, response, place_id):
#         #TODO get location users
#         pass
#
#     def get_location_users_json(self, place_id):
#         pass
#
#
# class LocationGroups(object):
#     def __init__(self):
#         pass
#
#     def on_get(self, request, response, place_id):
#         #TODO get location groups
#         pass
#
#     def get_location_groups_json(self, place_id):
#         pass
#
#
# class LocationOrganizations(object):
#     def __init__(self):
#         pass
#
#     def on_get(self, request, response, place_id):
#         #TODO get location organizations
#         pass
#
#     def get_location_groups_json(self, place_id):
#         pass