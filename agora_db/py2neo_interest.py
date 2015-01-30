__author__ = 'Marnee Dearman'
import uuid

from py2neo import Graph, Node

# from py2neo import neo4j
from agora_types import AgoraLabel


class AgoraInterest(object):
    def __init__(self, graph_db=None):
        self.name = None
        self.id = None
        self.description = None
        self.graph_db = Graph()
        #neo4j.GraphDatabaseService("http://localhost:7474/db/data/")

    @property
    def interest_properties(self):
        properties_dict = dict(self.__dict__)
        del properties_dict['graph_db']
        return properties_dict

    @property
    def interest_node_by_id(self):
        if not self.id is None:
            return self.graph_db.find_one(AgoraLabel.INTEREST,
                                          property_key='id',
                                          property_value=self.id)
        else:
            return None

    @property
    def interest_node_by_name(self):
        if not self.name is None:
            return self.graph_db.find_one(AgoraLabel.INTEREST,
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
        #TODO -- create as indexed node?
        self.id = str(uuid.uuid4())

        new_interest_node = Node.cast(AgoraLabel.INTEREST, self.interest_properties)
        try:
            self.graph_db.create(new_interest_node)
        except:
            pass

        return new_interest_node

        # interest_node = self.get_interest()
        # if interest_node is None:
        #     self.id = str(uuid.uuid4())
        #     new_interest = neo4j.Node.abstract(name=self.name, desciption=self.description, id=self.id)
        #     created_interest, = self.graph_db.create(new_interest)
        #     created_interest.add_labels(AgoraLabel.INTEREST)
        #     return created_interest
        # else:
        #     return interest_node

    def get_interest_by_name(self):
        """
        get interest node
        :return:
        """
        interest_node = self.interest_node_by_name

        if not interest_node is None:
            interest_attributes = self.interest_properties
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