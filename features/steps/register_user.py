__author__ = 'Marnee Dearman'

import httplib

from behave import when, then, given


@given(u'I am a new user')
def step_impl(context):
    # this is where I do something?  I dont know.
    #setup a non-registered user?  to use in the rest of the tests.  can I do that here
    raise NotImplementedError(u'STEP: Given I am a new user')


@when(u'I POST to URL "/users" with the body')
def step_impl(context):
    user_json = {
        "users": {
            "email": "email@example.com"
        }
    }

    # application/json
    headers = {"Content-type": "application/json",
               "Accept": "application/json"}
    conn = httplib.HTTPConnection("localhost", "8000")
    conn.request("POST", "/users", user_json, headers)
    # raise NotImplementedError(u'STEP: When I POST to URL "/users" with the body')


@then(u'I should get a 201 Created status code')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should get a 201 Created status code')
