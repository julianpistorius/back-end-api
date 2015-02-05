__author__ = 'Marnee Dearman'
from py2neo import Node, Graph, Relationship
from agora_db.py2neo_user import AgoraUser

interest_node = Graph().find_one('INTEREST',
                                 property_key='name',
                                 property_value='Kettlebells')
user_node = Graph().find_one('USER',
                             property_key='email',
                             property_value='marnee@agorasociety.com')

location_node = Graph().find_one('LOCATION',
                                 property_value='Tucson',
                                 property_key='name')

goal_node = Graph().find_one('GOAL',
                             property_value='',
                             property_key='id')

# user_interest_relationship = Relationship(start_node=user_node,
#                                                rel='INTERESTED_IN',
#                                                end_node=interest_node)

user_interest_rel = Graph().match_one(start_node=user_node,
                                     rel_type='INTERESTED_IN',
                                     end_node=interest_node)

# print user_interest_rel
for rel in user_interest_rel:
    print rel.rel['experience']
    print rel.rel['time']

#
# user_location_relationship = Relationship(start_node=user_node,
#                                           rel='LOCATED_IN',
#                                           end_node=location_node)

#update the node property
# user_properties = user_node.properties
# user_properties['mission_statement'] = 'New mission statement'
# # user_node.bind(uri=Graph().uri)
# user_node.push()
#
# #update the relationship property
#
# # user_interest_relationship['experience'] = 'descirption'
# #this does not work TODO ask on Stack Overflow
# # user_interest_relationship.bind(uri=Graph().uri)
# # user_interest_relationship.push()
# # print user_properties
#
# props = {'experience': 'Beginner level.',
#          'time': '3 years'}
#
# for key, value in props.iteritems():
#     user_interest_rel.properties[key] = value
# user_interest_rel.push()
#
# # Graph().create_unique(user_interest_relationship)
# # Graph().create_unique(user_location_relationship)
#
# # list_of_rels = []
# # list_of_rels.append('LOCATED_IN')
# # list_of_rels.append('INTERESTED_IN')
# # # start_node = Node('USER')
# # # start_node.bind(Graph().uri)
# # relate = Graph().match(start_node=None,
# #                        rel_type=list_of_rels,
# #                        end_node=None)
#
# # list_of_nodes = []
# # # print list(relate)
# # for rel in relate:
# #     # print rel.nodes
# #     relationships = rel.relationships
# #     for rel1 in relationships:
# #         print 'user', rel.start_node['name'], 'type', rel1.type, 'user', rel.end_node['name']
# #     list_of_nodes.append(rel.end_node)  #.properties['name']
# # for node in list_of_nodes:
#     # print node
#
# # print '*******AgoraUser: get_users_shared_interests_near_location cypher query'
# # user = AgoraUser()
# # user.email = "marnee@agorasociety.com"
# # print user.get_local_users_shared_interests_near_location(location_node)
#
# # for record in r:
# #     print record[0]
# # print r
# # print r.to_subgraph()
# # print r['o']
# # print r['email']
#
# #delete relationships and nodes
# user_goal_rel = Graph().match_one(start_node=user_node,
#                                   rel_type='HAS_GOAL',
#                                   end_node=goal_node)
# Graph().delete(user_goal_rel)