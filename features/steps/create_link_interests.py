__author__ = 'Marnee Dearman'
import sys
import os
from jsonschema import validate
from behave import when, given, then
from itsdangerous import URLSafeTimedSerializer
import requests
import falcon
import settings
from py2neo import Graph, Node, Relationship
from agora_api.users import AgoraUser

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

@given(u'interest entity from persona "interest"')
def setup_interest(context):
    interest = context.personas['interest']
    context.interest_json = {
        "interests": [
            {
                "name": interest['name'],
                "description": interest['description'],
                "experience": interest['experience'],
                "time": interest['time']
            }
        ]
    }

@given(u'entity persona "marnee"')
def setup_marnee(context):
    context.entity = context.personas['marnee']

@given(u'entity persona "group"')
def setup_group(context):
    context.entity = context.personas['group']

@given(u'route to entity')
def setup_route(context):
    context.route = context.entity['interest_route']

@when(u'the client requests POST to entity route with the body')
def post_interest_to_entity(context):
    context.response = requests.post(url=context.base_url + context.route, json=context.interest_json)

@then(u'the response is 201 created status code')
def check_response(context):
    assert context.response.status_code == 201, \
        'status code: %s != %s' % (context.response.status_code, falcon.HTTP_201)

@then(u'the "interest" is created and linked to the entity')
def check_interest_created_linked(context):
    entity = Graph(settings.DATABASE_URL).find_one(context.entity['label'],
                                                   property_key=context.entity['key'],
                                                   property_value=context.entity[context.entity['key']])
    interest = Graph(settings.DATABASE_URL).find_one('INTEREST', property_key='name',
                                                     property_value=context.personas['interest']['name'])
    for relationship in Graph(settings.DATABASE_URL).match(start_node=entity, rel_type='INTERESTED_IN', end_node=interest):
        assert relationship is not None