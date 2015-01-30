__author__ = 'Marnee Dearman'
from py2neo import Relationship, Node, Graph, LabelSet, PropertySet
from agora_db.py2neo_user import AgoraUser

# add password to use properties
# how to encrypt and decrypt the password
user = AgoraUser()
user.email = "marnee@agorasociety.com"
user.get_user()
user_node = user.user_node
print user_node

user.temp_auth_token = '666666666'
user.update_user()

print user.user_node

