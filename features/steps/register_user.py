__author__ = 'Marnee Dearman'

import sys
import os
from jsonschema import validate
import requests
import settings
from behave import when, then, given


@given(u'the user is new user with persona "new_user"')
def new_user(context):
    context.user = context.personas['new_user']

@given(u'the user is existing user with persona "marnee"')
def existing_user(context):
    context.user = context.personas['marnee']

@when(u'the client requests POST to route "/users" with the body')
def step_impl(context):
    user_json = {
        "user": {
            "email": context.user['email']
        }
    }
    # application/json
    headers = {"Content-type": "application/json",
               "Accept": "application/json"}
    context.response = requests.post(url=context.base_url + "/users", json=user_json)

@then(u'the response code is 201 Created')
def step_impl(context):
    assert context.response.status_code == 201, \
        "status code: %s != %s" % (context.response.status_code, '201')
