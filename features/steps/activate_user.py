__author__ = 'Marnee Dearman'
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

@given(u'an activation URL')
def an_activation_url(context):
    context.activation_url = context.base_url + settings.ACTIVATION_ROUTE

@given(u'email for persona "new_user"')
def step_impl(context):
    context.activation_email = context.personas['new_user']['email']

# @given(u'I have an activation URL with valid token')
@given(u'URL payload is valid')
def step_impl(context):
    s = URLSafeTimedSerializer(secret_key=settings.TOKEN_SECRET_KEY)
    context.payload = s.dumps(context.activation_email)

@when(u'Client POST to "/users/activation" with body')
def post_activation_url(context):
    # activation_url_with_payload = context.activation_url + "/" + context.payload
    context.json = {
        "user": {
            "email": context.activation_email,
            "payload": context.payload
        }
    }
    context.response = requests.post(url=context.activation_url, json=context.json)


@then(u'The response should be HTTP 201 Created')
def post_activation_response(context):
    response = context.response
    status_code = response.status_code
    assert status_code == 201, "status code: %s != %s" % (status_code, falcon.HTTP_201)


@then(u'The response is valid according to the "activated_user" schema')
def step_impl(context):
    activated_user_response_json = context.response.json()
    schema = {
        "$schema": "http://json-schema.org/draft-04/schema#",
        "id": "",
        "type": "object",
        "properties": {
            "user": {
                "id": "/user",
                "type": "object",
                "properties": {
                    "permanent_web_token": {
                        "id": "/user/permanent_web_token",
                        "type": "string"
                    },
                    "id": {
                        "id": "/user/id",
                        "type": "string"
                    }
                },
                "required": [
                    "permanent_web_token",
                    "id"
                ]
            }
        },
        "required": [
            "user"
        ]
    }
    validate(activated_user_response_json, schema)

@given(u'URL payload is invalid')
def invalid_token(context):
    s = URLSafeTimedSerializer(secret_key=settings.TOKEN_SECRET_KEY)
    context.payload = s.dumps('bad-email')

@then(u'The response should be 400 Bad request')
def step_impl(context):
    assert context.response.status_code == 400, \
        "status code: %s != %s" % (context.response.status_code, falcon.HTTP_400)
