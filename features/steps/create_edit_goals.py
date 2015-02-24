__author__ = 'Marnee Dearman'


@given(u'I am a registered user with a valid permanent web token')
def step_impl(context):
    raise NotImplementedError(u'STEP: Given I am a registered user with a valid permanent web token')

@when(u'I POST to URL "/users/{user_id}/goals" with the body')
def step_impl(context):
    raise NotImplementedError(u'STEP: When I POST to URL "/users/{user_id}/goals" with the body')

@then(u'The response is valid according to the "users" schema')
def step_impl(context):
    raise NotImplementedError(u'STEP: Then The response is valid according to the "users" schema')