__author__ = 'Marnee Dearman'
from py2neo import Node, Graph, Relationship
import uuid
import sys
import collections
#from py2neo import neo4j
from agora_db.agora_types import AgoraRelationship, AgoraLabel
from agora_db.py2neo_user import AgoraUser
from agora_db.py2neo_interest import AgoraInterest
graph_db = Graph()
id = str(uuid.uuid4())
email = "amy@agorasociety.com"
name = 'Amy'
new_user_properties = {
    "name": name,
    "mission_statement": "Use the Agora to learn all the things.",
    "id": id,
    "email": email.lower(),
    "is_mentor": True,
    "is_tutor": True,
    "is_visible": True,
    "is_available_for_in_person": True,
    "is_admin": False}
new_user_node = Node.cast(AgoraLabel.USER, new_user_properties)
try:
    graph_db.create(new_user_node)
except:
    print 'Node found'

user_node = graph_db.find_one(AgoraLabel.USER,
                                      property_key='email',
                                      property_value=email.lower())
print user_node["email"]

user = AgoraUser()
user.email = email
user.get_user()
print user.user_interests

interest = AgoraInterest()
interest.name = 'Music'
interest.description = 'Learning how to communicate clearly through writing.'
new_interest_node = interest.create_interest()
print new_interest_node
print user_node['name']
interest_node = Graph().find_one('INTEREST',
                                 property_key='name',
                                 property_value='Music')
user_interest_relationship = Relationship(start_node=user_node,
                                               rel=AgoraRelationship.INTERESTED_IN,
                                               end_node=interest_node)
print "rel:", user_interest_relationship
try:
    graph_db.create_unique(user_interest_relationship)
except Exception as e:
    print e.message

user.add_interest(new_interest_node)

print user.user_interests
