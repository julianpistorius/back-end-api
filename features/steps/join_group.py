__author__ = 'Marnee Dearman'

from behave import given, when, then
import requests
import falcon
import settings

@given(u'"group" group entity')
def setup_group(context):
    context.group = context.personas['group']

@given(u'"marnee" user entity')
def setup_user(context):
    context.entity = context.personas['marnee']
    # context.headers = ''

@given(u'route to join groups')
def setup_route(context):
    temp = context.entity['group_join_route']
    context.route = temp.format(user_id=context.entity['x_auth_key_good'],
                                group_id=context.group['id'])

@when(u'the client requests POST to join groups route')
def post_join(context):
    s = requests.Session()
    context.response = s.post(url=context.base_url + context.route,
                              headers=context.headers)

@then(u'the response is 201')
def check_response(context):
    assert context.response.status_code == 201, \
        'status code: %s != %s' % (context.response.status_code, falcon.HTTP_201)

@then(u'the response is valid according to the "user_joined" schema')
def validate_response_data(context):
    raise NotImplementedError(u'STEP: Then the response is valid according to the "user_joined" schema')

@then(u'"marnee" is a member of "group"')
def check_user_is_member(context):
    raise NotImplementedError(u'STEP: Then "marnee" is a member of "group"')

@then(u'response is 401')
def check_failure_response(context):
    raise NotImplementedError(u'STEP: Then response is 401')

@then(u'"marnee" is not a member of "group"')
def check_user_not_member(context):
    raise NotImplementedError(u'STEP: Then "marnee" is not a member of "group"')
