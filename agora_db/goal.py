__author__ = 'Marnee Dearman'
import py2neo
import datetime
import sys
import uuid
import settings
import collections
from py2neo import Graph, Node, Relationship, Path
from interest import AgoraInterest
from agora_types import AgoraRelationship, AgoraLabel

class AgoraGoal(object):
    def __init__(self):
        self.title = None
        self.id = None
        self.description = None
        self.start_date = None
        self.end_date = None
        self.created_date = None
        self.is_public = True
        self.achieved = False
        # self.interests = [] #list of interest dictionaries id:value
        self.graph_db = Graph(settings.DATABASE_URL)

    @property
    def goal_properties(self):
        goal_properties = dict(self.__dict__)
        del goal_properties['graph_db']
        return goal_properties

    @property
    def goal_node(self):
        """
        get a single goal node based on the attributes of the goal
        :return: neo4j.Node
        """
        goal_node = self.graph_db.find_one(AgoraLabel.GOAL,
                                           property_key='id',
                                           property_value=self.id)
        return goal_node

    @property
    def goal_interests(self):
        goal_interests = self.graph_db.match(start_node=self.goal_node,
                                             rel_type=AgoraRelationship.GOAL_FOR,
                                             end_node=None)
        goal_interests_list = []
        for rel in goal_interests:
            interest = AgoraInterest()
            interest.id = rel.end_node['id']
            goal_interests_list.append(interest.interest_properties)

        return goal_interests_list

    def set_goal_properties(self, goal_properties):
        for key, value in goal_properties.iteritesm():
            setattr(self, key, value)

    def create_goal(self):
        """
        create a goal and relate to user
        :return: neo4j.Node
        """
        # goal_node = self.get_goal()
        # #TODO get goal to prevent duplication?  maybe not needed -- MMMD 11/12/2014
        # if goal_node is None:
        self.id = str(uuid.uuid4())
        self.created_date = datetime.date.today()
        new_goal_properties = {}
        goal_attributes = dict(self.goal_properties)
        # print goal_attributes
        for key, value in goal_attributes.iteritems():
            new_goal_properties[key] = value


        # new_goal_properties = {
        #     "title": self.title,
        #     "description": self.description,
        #     "id": self.id,
        #     "start_date": self.start_date,
        #     "end_date": self.end_date,
        #     'created_date': datetime.date.today()}
        new_goal_node = Node.cast(AgoraLabel.GOAL, new_goal_properties)
        try:
            self.graph_db.create(new_goal_node)
            for interest in self.interests:
                self.add_interest(interest['id'])
        except:
            print sys.exc_info()
        return new_goal_node

    def update_goal(self):
        """
        update goal related to user
        :return:
        """
        goal_node = self.goal_node
        goal_properties = dict(self.goal_properties)

        for key, value in goal_properties.iteritems():
            goal_node[key] = value
        goal_node.push()

    def add_achievement(self):
        pass

    def get_goals_for_interest(self, interest_id):
        pass
        # interest = AgoraInterest()
        # interest.id = interest_id
        # goal_interests_path = Path(interest.interest_node_by_id,
        #                            AgoraRelationship.GOAL_INTEREST, )
        # interest_goals_relationship = self.graph_db.pa


    def add_interest(self, interest_id):
        """
        add interest relationship to goal node
        :param interest_id:
        :return:
        """
        interest = AgoraInterest()
        interest.id = interest_id
        interest_node = interest.interest_node_by_id
        goal_interest_relationship = Relationship(self.goal_node,
                                                  AgoraRelationship.GOAL_FOR,
                                                  interest_node)
        self.graph_db.create_unique(goal_interest_relationship)

    def delete_all_interests(self):
        """
        delete all interest relationships
        :return:
        """
        goal_interests_rels = Relationship(self.goal_node,
                                           AgoraRelationship.GOAL_FOR,
                                           None)
        self.graph_db.delete(goal_interests_rels)

    def get_goal(self):
        goal_node = self.goal_node
        goal_properties = {}
        goal_properties = dict(goal_node.properties)
        if not goal_node is None:
            for key, value in goal_properties.iteritems():
                setattr(self, key, value)

    # def all_goals_for_json(self):
    #     return self.goal_properties
    #
    # def interest_goals_for_json(self, interest_id):
    #     pass

    def goal_for_json(self):
        root = {}
        root = self.goal_properties
        root['interests'] = self.goal_interests
        # root['id'] = self.id
        # root['title'] = self.title
        # root['description'] = self.description
        # root['is_public'] = self.is_public
        # root['start_date'] = self.start_date
        # root['end_date'] = self.end_date
        # root['created_date'] = self.created_date
        # root['interests'] = self.goal_interests
        return root