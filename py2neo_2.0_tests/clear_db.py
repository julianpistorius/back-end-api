__author__ = 'Marnee Dearman'
from agora_db.py2neo_user import AgoraUser
from agora_db.py2neo_interest import AgoraInterest
from agora_db.py2neo_goal import AgoraGoal
from agora_db.py2neo_group import AgoraGroup
from agora_db.py2neo_organization import AgoraOrganization
from agora_db.agora_types import AgoraRelationship, AgoraLabel
import py2neo
#from py2neo import neo4j
import datetime

import time

graph_db = py2neo.Graph("http://localhost:7474/db/data/")
#start over seeding the database
graph_db.delete_all()
