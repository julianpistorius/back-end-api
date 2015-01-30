__author__ = 'Marnee Dearman'
from py2neo import Node, Graph, Relationship
import uuid
import collections
#from py2neo import neo4j
from agora_db.py2neo_group import AgoraGroup
from agora_db.agora_types import AgoraLabel, AgoraRelationship
import datetime
graph_db = Graph()

name = "Tucson Startup Demo Day"

group_node_check = Graph().find_one(AgoraLabel.STUDYGROUP,
                                    property_key='name', property_value=name)

group = AgoraGroup()
if group_node_check is None:
    group.name = name
    group.description = "We meet to demo our systems & progress and talk about starting up"
    group.is_invite_only = True
    group.is_open = True
    group.meeting_location = "Co-Lab"
    group.next_meeting_date = datetime.date(2014, 12, 4)
    group.next_meeting_time = datetime.time(12, 30)
    group.group_leader_username = "Dan"

    group.create_group()
else:
    group.id = group_node_check.end_node["id"]
    group.get_group()

print group.group_node