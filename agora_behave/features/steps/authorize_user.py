__author__ = 'Marnee Dearman'

@given(u'I am a registered user')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given I am a registered user')

@when(u'I POST to URL "/login"')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I POST to URL "/login"')

@then(u'I should get a 202 Accepted response')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should get a 202 Accepted response')

@given(u'I go to the authorization URL from my email')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given I go to the authorization URL from my email')

@given(u'The token is valid')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given The token is valid')

@then(u'I should get a 200 OK response')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should get a 200 OK response')

@then(u'The response is valid according to the "authorized_user" schema')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then The response is valid according to the "authorized_user" schema')

@given(u'I got to the authorization URL')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given I got to the authorization URL')

@given(u'The token is not valid')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given The token is not valid')

@then(u'I should get a 303 See Other response to redirect to the registration page')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then I should get a 303 See Other response to redirect to the registration page')

@then(u'The response is valid according to the "redirect" schema')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then The response is valid according to the "redirect" schema')