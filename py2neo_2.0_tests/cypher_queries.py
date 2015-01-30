from py2neo import Graph, Path, Node, Relationship
from agora_db.agora_types import AgoraLabel, AgoraRelationship


#user goals and interests

params = {
    'email': 'marnee@agorasociety.com'
}

cypher_string = "match (u:USER {email:{email}})-[r:HAS_GOAL]->(g:GOAL)-[rg:GOAL_FOR]->(i:INTEREST) " \
              " return u.name as user, g.title as goal, i.name as interest"

data = Graph().cypher.execute(cypher_string, params)
print data

params = {
    'email': 'marnee@agorasociety.com'
}
cypher_str = "MATCH (u:USER {email:{email}})-[url:LOCATED_IN]->(l:LOCATION)"
cypher_str += "<-[orl:LOCATED_IN]-(o:USER) "
cypher_str += "WITH u, o, l, url, orl "
cypher_str += "MATCH (u)-[ru:INTERESTED_IN]->"
cypher_str += "(i:INTEREST)<-[ro:INTERESTED_IN]-(o) "
cypher_str += "RETURN i.name as interest_name, i.id as interest_id, " \
              "o.name as user_name, o.id as user_id" #, u, ru, ro, l, url, orl"
# print cypher_str
results = Graph().cypher.execute(cypher_str, params)
print results