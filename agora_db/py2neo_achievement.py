__author__ = 'Marnee Dearman'
import uuid

from py2neo import Graph, Node

from agora_types import AgoraRelationship, AgoraLabel

class AgoraAchievement(object):
    def __init__(self, graph_db):
        self.name = None
        self.id = None
        self.description = None
        self.title = None
        self.is_visible = True
        self.date = None
        self.graph_db = Graph()

    @property
    def achievement_node(self):
        return self.graph_db.find_one(AgoraLabel.ACHIEVEMENT,
                                      property_key='id',
                                      property_value=self.id)

    @property
    def achievement_interests(self):
        """
        get list of interests linked to this achievement
        :return:
        """
        # ach_interests = self.graph_db.match(start_node=self.achievement_node,
        #                                     rel_type=AgoraRelationship.)
        pass
