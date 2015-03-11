__author__ = 'marnee'
from behave import given, then, when
import requests
import falcon
import settings
from jsonschema import validate
import json

@given(u'search string "Mar"')
def setup_user_string(context):
    context.search_str = "Mar"
    context.entity = context.personas['user']


@given(u'search string "Tuc"')
def setup_group_string(context):
    context.search_str = "Tuc"
    context.entity = context.personas['group']


@given(u'search string "ket"')
def setup_interest_string(context):
    context.search_str = "ket"
    context.entity = context.personas['interest']


@given(u'route to entity search')
def route_to_entity_search(context):
    temp = context.entity['entity_search_route']  # context.personas['entity_search'][context.entity]
    context.route = temp.format(match=context.search_str,
                                limit='10')


@when(u'the client requests GET from entity route with parameters')
def get_results(context):
    s = requests.Session()
    context.response = s.get(url=context.base_url + context.route)


@then(u'the response is 200')
def check_response(context):
    assert context.response.status_code == 200, \
        'status code %s != %s' % (context.response.status_code, falcon.HTTP_200)


@then(u'the response is valid according to the "entity_search_results" schema')
def check_response_schema(context):
    response_data = context.response.json()
    with open(context.entity['search_schema']) as schemafile:
        schema = json.load(schemafile)
        schemafile.close()
    validate(response_data, schema)

