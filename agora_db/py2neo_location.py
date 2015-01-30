__author__ = 'Marnee Dearman'
import uuid

from py2neo import Node, Graph, Relationship

from agora_types import AgoraRelationship, AgoraLabel

class AgoraLocation(object):
    def __init__(self):
        self.formatted_address = None
        self.name = None
        # self.postal_code = None
        # self.country = False
        # self.locality = True
        self.id = None  #place_id
        self.graph_db = Graph()

    @property
    def location_properties(self):
        props = dict(self.__dict__)
        del props['graph_db']
        return props

    @property
    def location_node_by_name(self):
        """
        get a location node by location name
        :return: py2neo node
        """
        return self.graph_db.find_one(AgoraLabel.LOCATION,
                                      property_key='name',
                                      property_value=self.name)
    @property
    def location_node_by_place_id(self):
        """
        get a location node by the place_id
        :return: py2neo Node
        """
        return self.graph_db.find_one(AgoraLabel.LOCATION,
                                      property_key='place_id',
                                      property_value=self.place_id)

    def create_location(self):
        self.id = str(uuid.uuid4())
        # new_location_properties = {
        #     "formatted_address": self.formatted_address,
        #     "name": self.name,
        #     "place_id": self.place_id
        # }
        new_location_node = Node.cast(AgoraLabel.LOCATION, self.location_properties)
        try:
            self.graph_db.create(new_location_node)
        except:
            pass
        return new_location_node

    def get_location(self):
        location_node = self.location_node_by_place_id
        location_properties = {}
        location_properties = dict(location_node.properties)
        if not location_node is None:
            for key, value in location_properties.iteritems():
                setattr(self, key, value)

