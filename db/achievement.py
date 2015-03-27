__author__ = 'Marnee Dearman'
import uuid
import settings

from py2neo import Graph, Node

from labels_relationships import GraphRelationship, GraphLabel

class Achievement(object):
    def __init__(self, graph_db):
        self.name = None
        self.id = None
        self.description = None
        self.title = None
        self.is_visible = True
        self.date = None
        self._graph_db = Graph(settings.DATABASE_URL)

    @property
    def achievement_node(self):
        return self._graph_db.find_one(GraphLabel.ACHIEVEMENT,
                                      property_key='id',
                                      property_value=self.id)

    @property
    def achievement_interests(self):
        """
        get list of interests linked to this achievement
        :return:
        """
        # ach_interests = self.graph_db.match(start_node=self.achievement_node,
        #                                     rel_type=Relationship.)
        return None
