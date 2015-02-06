__author__ = 'Marnee Dearman'
from py2neo import Node, Graph, Relationship
import uuid
import collections
#from py2neo import neo4j
from agora_db.agora_types import AgoraRelationship, AgoraLabel
from agora_db.py2neo_user import AgoraUser
from agora_db.py2neo_interest import AgoraInterest
from agora_db.py2neo_location import AgoraLocation
graph_db = Graph()
id = str(uuid.uuid4())

#create location
new_location = AgoraLocation()
new_location.formatted_address = "Bisbee, AZ 85603, USA"
new_location.name = "Bisbee"
new_location.place_id = "ChIJL9jhHLi00IYRGms2fEz_zGU"

try:
    new_location.create_location()
except:
    pass

new_location_node = new_location.location_node
print new_location_node
# user = AgoraUser()
# user.email = "marnee@agorasociety.com"
# user.get_user()
#
# user.add_location(new_location_node)
#
# print user.user_locations




#add location to user

