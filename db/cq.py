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

