__author__ = 'Marnee Dearman'
import uuid
import settings
from py2neo import Graph, Node

# from py2neo import neo4j
from labels_relationships import GraphLabel


class Interest(object):
    def __init__(self, graph_db=None):
        self.name = None
        self.id = None
        self.description = None
        self._graph_db = Graph(settings.DATABASE_URL)

    @property
    def interest_properties(self):
        properties_dict = dict(self.__dict__)
        del properties_dict['_graph_db']
        return properties_dict

    @property
    def interest_node_by_id(self):
        if not self.id is None:
            return self._graph_db.find_one(GraphLabel.INTEREST,
                                          property_key='id',
                                          property_value=self.id)
        else:
            return None

    @property
    def interest_node_by_name(self):
        if self.name is not None:
            return self._graph_db.find_one(GraphLabel.INTEREST,
                                  property_key='name',
                                  property_value=self.name)
        else:
            return None

    def set_interest_attributes(self, interest_properties):
        for key, value in interest_properties.iteritems():
            setattr(self, key, value)

    def create_interest(self):
        """
        create an interest node based on the class attributes
        :return: py2neo Node
        """
        #TODO error handling
        self.id = str(uuid.uuid4())
        new_interest_node = Node.cast(GraphLabel.INTEREST, self.interest_properties)
        try:
            self._graph_db.create(new_interest_node)
        except:
            pass

        return new_interest_node

        # interest_node = self.get_interest()
        # if interest_node is None:
        #     self.id = str(uuid.uuid4())
        #     new_interest = neo4j.Node.abstract(name=self.name, desciption=self.description, id=self.id)
        #     created_interest, = self.graph_db.create(new_interest)
        #     created_interest.add_labels(GraphLabel.INTEREST)
        #     return created_interest
        # else:
        #     return interest_node

    def matched_interests(self, match_string, limit):
        params = {
            'match': '(?i)%s.*' % match_string,
            'limit': limit
        }
        cypher_str = "MATCH (interest:INTEREST ) " \
            "WHERE interest.name =~ {match} " \
            "RETURN interest.name as name, interest.id as id " \
            "LIMIT {limit}"
        match_results = self._graph_db.cypher.execute(statement=cypher_str, parameters=params)
        root = {}
        root['count'] = 0
        interest_found = {}
        interests_list = []
        for item in match_results:
            interest_found['id'] = item.id
            interest_found['name'] = item.name
            # self.id = item['id']
            # self.get_user()
            # users_list.append(dict(self.user_properties))
            interests_list.append(dict(interest_found))
            root['count'] += 1
        root['interests'] = interests_list
        return root

    def get_interest_by_name(self):
        """
        get interest node
        :return:
        """
        interest_node = self.interest_node_by_name

        if interest_node is not None:
            interest_attributes = dict(interest_node.properties)
            for key, value in interest_attributes.iteritems():
                setattr(self, key, value)
        return interest_node

    def get_interest_by_id(self):
        interest_node = self.interest_node_by_id

        if not interest_node is None:
            interest_attributes = self.interest_properties
            for key, value in interest_node.properties.iteritems():
                setattr(self, key, value)
        return interest_node

    def get_interest_for_json(self):
        root = {}
        return {
            '__class': self.__class__.__name__,
            'id': self.id,
            'name': self.name
        }

    # def get_interest_by_id(self):
    #     """
    #     get interest node by unique id
    #     sets attributes of this interest instance to properties on node found
    #     :return: noe4j.Node
    #     """
    #     interest_node = self.interest_node_by_id
    #     if not interest_node is None:
    #         self.name = interest_node["name"]
    #         self.id = interest_node["id"]
    #         self.description = interest_node["description"]
    #
    #     return interest_node

