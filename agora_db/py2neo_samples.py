__author__ = 'Marnee Dearman'
import py2neo
from py2neo import neo4j

graph_db = neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

# #get a user name
# node = graph_db.find("User", "email", "ralphie@email.com")
# node_list = list(node)
# print node_list
#
# nodes_list = graph_db.find("User", "email", "ralphie@email.com")
# #print (len(list(nodes_list)))
# node = nodes_list.next()
# print node["name"]
#node = nodes_list.next()



new_indexed_node = graph_db.get_or_create_indexed_node(index_name='User', key='email', value="ralphie@email.com", properties={'id': '7e0570a4-15db-4b45-8085-88135334876e'})
indexes = graph_db.get_indexes(neo4j.Node)
print indexes
# graph_db.delete(new_indexed_node) #this deletes the index too.  sure wish this was in the documenfuckingtation
# indexes = graph_db.get_indexes(neo4j.Node)
# print indexes
# graph_db.get_index(neo4j.Node, 'User')


# print new_indexed_node
# new_indexed_node.add_labels("User")

# graph_db.delete_index(new_indexed_node, 'User')


#get a study group
# for node in graph_db.find("STUDYGROUP", "name", "Agora Motorcycle Riders"):
#     print node
#     print node["name"]
#     properties = node.get_properties()
#     print properties
#
# #get nodes by label
# for user_node in graph_db.find("User"):
#     print "by labels", user_node
#
# #get indexes
# indexes = graph_db.get_indexes(neo4j.Node)
# print 'indexes', indexes
#
# user_nodes = graph_db.find("User", "name", "Marnee")
# user_node = user_nodes.next()
#
# interest_nodes = graph_db.find("INTEREST", "name", "Medical Research")
# interest_node = interest_nodes.next()
#
# #get all relationships
# user_interests = graph_db.match(start_node=user_node, rel_type="INTERESTED_IN", end_node=None)
# for item in user_interests:
#     print "relationships", item.__dict__
#     print item.start_node["name"]
#     print item.end_node["name"]
# #study_group = graph_db.get_or_create_index(neo4j.Node, "study_group")
#
# #create a relationship INTERESTED_IN
# neo4j.Path(user_node, "INTERESTED_IN", interest_node).get_or_create(graph_db)
# #print "new relationship from path", new_relationship
#
#
# #get all relationships
# user_interests = graph_db.match(start_node=user_node, rel_type="INTERESTED_IN", end_node=None)
# for item in user_interests:
#     print "new relationships", item.__dict__
#     print item.start_node["name"]
#     print item.end_node["name"]