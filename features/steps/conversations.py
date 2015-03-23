__author__ = 'marnee'
import sys
import os
from jsonschema import validate
from behave import when, given, then
from itsdangerous import URLSafeTimedSerializer
import requests
import falcon
import settings

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')


@given(u'start conversation group entity')
def step_impl(context):
    context.group = context.personas['group']

@given(u'start conversation user entity')
def step_impl(context):
    context.convo_started = context.personas['julian']

@given(u'conversation with user entity')
def step_impl(context):
    context.conv_with = context.personas['marnee']

@given(u'"conversation" conversation entity')
def step_impl(context):
    context.conversation = {
        'conversation': dict(
            subject='TEST CONVERSATION',
            message='TEST MESSAGE'
        )
    }

@given(u'route to user conversation resource')
def step_impl(context):
    temp = context.convo_with['conversation_route']
    context.route = temp.format(user_id=context.convo_with)

@given(u'the request to POST a conversation contains a good x-auth-key')
def step_impl(context):
    context.headers = context.convo_started['x_auth_key_good']

@when(u'the client requests POST to start a new conversation')
def step_impl(context):
    s = requests.Session()
    context.response = s.post(url=context.base_url + context.route,
                              headers=context.headers)

@then(u'the response to starting a conversation is 201')
def step_impl(context):
    assert context.response.status_code == 201, \
        'status code: %s != %s' % (context.response.status_code, falcon.HTTP_201)

@then(u'the response is valid according to the "conversation" schema')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the response is valid according to the "conversation" schema')

@then(u'"marnee" has a conversation with "julian"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then "marnee" has a conversation with "julian"')

@then(u'"julian" has a conversation with "marnee"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then "julian" has a conversation with "marnee"')

@then(u'no new conversation have been created')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then no new conversation have been created')

@when(u'the client requests POST to respond to a conversation')
def step_impl(context):
    raise NotImplementedError(u'STEP: When the client requests POST to respond to a conversation')

@then(u'the response is valid according to the "response" schema')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the response is valid according to the "response" schema')

@then(u'"conversation" has a new response')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then "conversation" has a new response')

@then(u'response is by "julian"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then response is by "julian"')

@given(u'goal entity from persona "goal"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given goal entity from persona "goal"')

@given(u'user entity from persona "marnee"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given user entity from persona "marnee"')

@given(u'route to POST goals to user entity')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given route to POST goals to user entity')

@then(u'I should get a 201 Created status code')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should get a 201 Created status code')

@given(u'"marnee"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given "marnee"')

@given(u'"julian"')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given "julian"')

@when(u'the client requests POST to messaging route')
def step_impl(context):
    raise NotImplementedError(u'STEP: When the client requests POST to messaging route')

@then(u'the response code is 201 created')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the response code is 201 created')

@then(u'the response is valid according to the "messages" schema')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then the response is valid according to the "messages" schema')

@then(u'a message was logged')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then a message was logged')
