__author__ = 'Marnee Dearman'
import os
from behaving import environment as benv
from py2neo import Node, Graph
import settings
from agora_db import user

PERSONAS = {
    'new_user': dict(
        email='newuser@agorasociety.com'
    ),
    'marnee': dict(
        email='marnee@agorasociety.com'
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
    new_user_node = Node('USER', email='newuser@agorasociety.com')
    graph_db.delete(new_user_node)
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
