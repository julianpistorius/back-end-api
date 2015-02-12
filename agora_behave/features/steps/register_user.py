__author__ = 'Marnee Dearman'

import logging
import json
import base64

from behaving.personas.steps import given_a_persona
from behave import when, then, given

@given(u'I am a new user')
def step_impl(context):
    #this is where I do something?  I dont know.
    #setup a non-registered user?  or sommething
    raise NotImplementedError(u'STEP: Given I am a new user')

@when(u'I POST to URL "/users" with the body')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I POST to URL "/users" with the body')

@then(u'I should get a 201 Created status code')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should get a 201 Created status code')
