__author__ = 'marnee'

import uuid
import datetime
import sys
import settings
from py2neo import Node, Graph, Relationship, Path, Rev
from labels_relationships import GraphRelationship, GraphLabel
from db.user import User


#  PROBABLY DONT NEED THIS CLASS BUT WILL KEEP FILE FOR NOW -- MMD 3/16
class Response(object):
    def __init__(self):
        """

        :return:
        """
        self.id = ''
        self.message = ''
        self.sent_date = ''
        self.graph_db = Graph(settings.DATABASE_URL)

    @property
    def response_properties(self):
        """

        :return:
        """
        properties_dict = dict(self.__dict__)
        del properties_dict['graph_db']
        return properties_dict

    @property
    def response_node(self):
        """

        :return:
        """
        if self.id != '':
            return self.graph_db.find_one(GraphLabel.RESPONSE,
                                          property_key='id',
                                          property_value=self.id)

    def create_response(self):
        pass

    # def add_response(self):

    # @property
    # def conversation(self):
    #     return self.graph_db
    #

    # @property
    # def to_entity(self):
    #     """
    #
    #     :return:
    #     """
    #     message_to_relationship = self.graph_db.match(start_node=self.response_node,
    #                                                   rel_type=GraphRelationship.TO,
    #                                                   end_node=None)
    #     to_list = []
    #     for rel in message_to_relationship:
    #         user = rel.end_node.properties
    #         to_list.append(user)
    #     return to_list

    # @property
    # def from_entity(self):
    #     """
    #
    #     :return:
    #     """
    #     message_from_relationship = self.graph_db.match(start_node=None,
    #                                                     rel_type=GraphRelationship.SENT,
    #                                                     end_node=self.message_node)
    #     for rel in message_from_relationship:
    #         entity =