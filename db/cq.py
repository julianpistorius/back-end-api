from db.user import User

__author__ = 'marnee'

import uuid
import datetime
import sys
import settings
from py2neo import Node, Graph, Relationship, Path, Rev
from labels_relationships import GraphRelationship, GraphLabel


class Cq(object):
    def __init__(self):
        """

        :return:
        """
        self.id = ''
        self.subject = ''
        self.message = ''
        self.created_date = ''
        self.graph_db = Graph(settings.DATABASE_URL)

    @property
    def cq_properties(self):
        """

        :return:
        """
        properties_dict = dict(self.__dict__)
        del properties_dict['graph_db']
        return properties_dict

    @property
    def cq_node(self):
        """

        :return:
        """
        if self.id != '':
            return self.graph_db.find_one(GraphLabel.CQ,
                                          property_key='id',
                                          property_value=self.id)

    @property
    def response_list(self):
        """
        list of responses to this CQ
        :return: list of responses
        """
        cq_response_relationship = self.graph_db.match(start_node=self.cq_node,
                                                       rel_type=GraphRelationship.TO,
                                                       end_node=None)
        response_list = []
        for rel in cq_response_relationship:
            response = rel.end_node.properties
            user_response_relationship = self.graph_db.match_one(start_node=None,
                                                                 rel_type=GraphRelationship.RESPONDED,
                                                                 end_node=self.cq_node)
            user_node = user_response_relationship.start_node
            response['by'] = '%s / %s' % (user_node.properties['name'],
                                          user_node.properties['call_sign'])
            response_list.append(response)

        return response_list

    def create_cq(self, user_id):
        self.id = str(uuid.uuid4())
        self.created_date = datetime.date.today()
        cq_node = Node.cast(GraphLabel.CQ,
                            self.cq_properties)
        self.graph_db.create(cq_node)
        user = User()
        user.id = user_id
        cq_user_relationship = Relationship(user.user_node,
                                            GraphRelationship.SENT,
                                            cq_node)
        self.graph_db.create_unique(cq_user_relationship)

    def response(self, response_id):
        """
        response dictionary details including user details
        :param response_id:
        :return:  dict with response details and a dict of the user who made the response
        """
        response_node = self.graph_db.find_one(GraphLabel.RESPONSE,
                                               property_key='id',
                                               property_value=response_id)
        response_user_relationship = self.graph_db.match_one(start_node=None,
                                                             rel_type=GraphRelationship.RESPONDED,
                                                             end_node=response_node)
        response_dict = {}
        response_dict['response'] = response_node.auto_sync_properties
        response_dict['user'] = response_user_relationship.start_node.properties
        return response_dict