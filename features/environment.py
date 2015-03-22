__author__ = 'Marnee Dearman'
import os
from behaving import environment as benv
from py2neo import Node, Graph, Relationship
import settings
from db import user

PERSONAS = {
    'user': dict(
        email='newuser@elmerly.com',
        entity_search_route='/users?match={match}&limit={limit}',
        search_schema='schemas/user_search_results.json'
    ),
    'marnee': dict(
        email='marnee@elmerly.com',
        interest_route='/users/{id}/interests',
        label='USER',
        key='email',
        x_auth_key_good='IjA5ZGViOWY0LTZmZWItNDJlNC1iY2YyLTU1ZjgyYzI2NjMyZiI.VnlgmEXwW9eelZT5Xbs6uPtPQJE',
        id='09deb9f4-6feb-42e4-bcf2-55f82c26632f',
        x_auth_key_bad='bad',
        group_join_route='/users/{user_id}/groups/{group_id}',
        conversation_route='/users/{user_id}/conversations'

    ),
    'julian': dict(
        email='julian@elmerly.com',
        interest_route='/users/{id}/interests',
        label='USER',
        key='email',
        x_auth_key_good='Ijg3MWZiYzYwLWJlYjgtNDUxMS04M2ZkLTJkOWU2MGMzMGZhOCI.B-9_JA.s_Jb4NBtk5Fwm-O4w1SNuMGBLPE',
        id='871fbc60-beb8-4511-83fd-2d9e60c30fa8',
        x_auth_key_bad='bad',
        group_join_route='/users/{user_id}/groups/{group_id}',
        conversation_route='/users/{user_id}/conversations'
    ),
    'group': dict(
        id='7e7ce64b-08d8-4df1-82ac-f0456bc7df15',
        interest_route='/groups/{id}/interests',
        label='STUDYGROUP',
        key='id',
        x_auth_key_good='IjA5ZGViOWY0LTZmZWItNDJlNC1iY2YyLTU1ZjgyYzI2NjMyZiI.VnlgmEXwW9eelZT5Xbs6uPtPQJE',
        x_auth_key_bad='bad',
        entity_search_route='/groups?match={match}&limit={limit}',
        search_schema='schemas/group_search_results.json',
        conversations_route='/users/{user_id}/conversations'

    ),
    'interest': dict(
        name='New Interest',
        description='New interests testing',
        experience='Just adding a test interest',
        time='100 years',
        entity_search_route='/interests?match={match}&limit={limit}',
        search_schema='schemas/interest_search_results.json'

    ),
    'entity_search': dict(
        user='/users?match={match}&limit={limit}',
        group='/groups?match={match}&limit={limit}',
        interest='/interests?match={match}&limit={limit}',
        user_schema='schemas/user_search_results.json',
        interest_schema='schemas/interest_search_results.json',
        group_schema='schemas/group_search_results.json'
    )
}

def before_all(context):
    # import falcon_test
    # context.attachment_dir = os.path.join(os.path.dirname(falcon_test.__file__), 'tests/data')
    # context.sms_path = os.path.join(os.path.dirname(falcon_test.__file__), '../../var/sms/')
    # context.mail_path = os.path.join(os.path.dirname(falcon_test.__file__), '../../var/mail/')
    # clear database
    graph_db = Graph(settings.DATABASE_URL)
    # graph_db.delete_all()
    new_user_node = graph_db.find_one('USER',
                                      property_key='email',
                                      property_value='newuser@agorasociety.com')
    graph_db.delete(new_user_node)
    interest_node = graph_db.find_one('INTEREST', property_key='name',
                                      property_value=PERSONAS['interest']['name'])
    interest_relationships = graph_db.match(start_node=None,
                                            rel_type='INTERESTED_IN',
                                            end_node=interest_node)
    for relationship in interest_relationships:
        graph_db.delete(relationship)
    graph_db.delete(interest_node)
    context.base_url = "http://localhost:8000"
    benv.before_all(context)


def after_all(context):
    benv.after_all(context)


def before_feature(context, feature):
    benv.before_feature(context, feature)


def after_feature(context, feature):
    benv.after_feature(context, feature)


def before_scenario(context, scenario):
    benv.before_scenario(context, scenario)
    context.personas = PERSONAS

def after_scenario(context, scenario):
    benv.after_scenario(context, scenario)
