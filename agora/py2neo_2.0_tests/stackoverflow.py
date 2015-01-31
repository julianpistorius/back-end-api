__author__ = 'Marnee Dearman'
from py2neo import Graph
user_node = Graph().find_one('USER',
                             property_key='email',
                             property_value='marnee@agorasociety.com')
# user_properties['mission_statement'] = 'New mission statement'
# user_node.bind(uri=Graph().uri)
user_node.properties['mission_statement'] = 'New mission statement'
user_node.push()