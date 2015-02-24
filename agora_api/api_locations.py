__author__ = 'Marnee Dearman'
# import os
# import time
# import uuid
# import falcon_api
# import msgpack_pure
# from agora_db.py2neo_user import AgoraUser
from agora_db.location import AgoraLocation
import simplejson

def get_location(name=None, postal_code=None, place_id=None):
    #TODO return location by name or postal code
    if not name is None:
        return 'loc'
    elif not postal_code is None:
        return 'loc'
    elif not place_id is None:
        agora_location = AgoraLocation()
        agora_location.id = place_id
        agora_location.get_location()
        return agora_location

class Location(object):
    def __init__(self):
        pass

    def on_get(self, response, request, name, postal_code):
        #TODO get location node (is this something I need to do?)
        pass

class LocationInterests(object):
    def __init__(self):
        pass

    def on_get(self, requests, response, place_id):
        #TODO get location interests
        pass

    def get_location_interests_json(self, place_id):
        location = get_location(place_id=place_id)


class LocationUsers(object):
    def __init__(self):
        pass

    def on_get(self, request, response, place_id):
        #TODO get location users
        pass

    def get_location_users_json(self, place_id):
        pass


class LocationGroups(object):
    def __init__(self):
        pass

    def on_get(self, request, response, place_id):
        #TODO get location groups
        pass

    def get_location_groups_json(self, place_id):
        pass


class LocationOrganizations(object):
    def __init__(self):
        pass

    def on_get(self, request, response, place_id):
        #TODO get location organizations
        pass

    def get_location_groups_json(self, place_id):
        pass