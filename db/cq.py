__author__ = 'marnee'

import uuid
import datetime
import settings
from py2neo import Node, Graph, Relationship, Path, Rev
from labels_relationships import GraphRelationship, GraphLabel
from db.interest import Interest
from py2neo.ext.calendar import GregorianCalendar


class Cq(object):
    def __init__(self):
        """

        :return:
        """
        self.id = ''
        self.subject = ''
        self.message = ''
        self.created_time = ''
        self.last_updated_time = ''
        self._graph_db = Graph(settings.DATABASE_URL)

    @property
    def cq_properties(self):
        """

        :return:
        """
        properties_dict = dict(self.__dict__)
        del properties_dict['_graph_db']
        return properties_dict

    @property
    def cq_node(self):
        """

        :return:
        """
        if self.id != '':
            return self._graph_db.find_one(GraphLabel.CQ,
                                          property_key='id',
                                          property_value=self.id)

    @property
    def response_list(self):
        """
        list of responses to this CQ
        :return: list of responses
        """
        cq_response_relationship = self._graph_db.match(start_node=self.cq_node,
                                                       rel_type=GraphRelationship.TO,
                                                       end_node=None)
        response_list = []
        for rel in cq_response_relationship:
            response = rel.end_node.properties
            user_response_relationship = self._graph_db.match_one(start_node=None,
                                                                 rel_type=GraphRelationship.RESPONDED,
                                                                 end_node=self.cq_node)
            user_node = user_response_relationship.start_node
            response['by'] = '%s / %s' % (user_node.properties['name'],
                                          user_node.properties['call_sign'])
            response_list.append(response)

        return response_list

    @staticmethod
    def create_cq(user_node, cq_dict, cq_interests_list):
        """
        create the CQ node and link to the user and interests, also adds the date graph
        :param user_node:
        :param cq_dict:
        :param cq_interests_list:
        :return:
        """
        graph = Graph(settings.DATABASE_URL)
        cq_dict['id'] = str(uuid.uuid4())
        cq_dict['created_time'] = datetime.datetime.now().time()
        cq_dict['last_updated_time'] = datetime.datetime.now().time()
        cq_node = Node.cast(GraphLabel.CQ,
                            cq_dict)
        cq_node, = graph.create(cq_node)
        cq_relationship = Relationship(user_node,
                                       GraphRelationship.SENT,
                                       cq_node)
        Graph(settings.DATABASE_URL).create_unique(cq_relationship)

        for interest_id in cq_interests_list:
            interest = Interest()
            interest.id = interest_id
            cq_interest_relationship = Relationship(cq_node,
                                                    GraphRelationship.INTERESTED_IN,
                                                    interest.interest_node_by_id)
            graph.create_unique(cq_interest_relationship)

        calendar = GregorianCalendar(graph)
        cur_date = datetime.date.today()
        cq_on = Relationship(cq_node,
                             GraphRelationship.ON,
                             calendar.date(cur_date.year, cur_date.month, cur_date.day).day)
        graph.create_unique(cq_on)
        return cq_node

    @staticmethod
    def update_cq(user_node, cq_dict, cq_interests_dict):
        """

        :param user_node:
        :param cq_dict:
        :param cq_interests_dict:
        :return:
        """
        #TODO:  update node -- find out how to change the date graph
        pass

    @staticmethod
    def delete_cq(user_node, cq_id):
        cq = Cq()
        cq.id = cq_id
        graph = Graph(settings.DATABASE_URL)
        cq_rel = graph.match_one(start_node=user_node,
                        rel_type=GraphRelationship.SENT,
                        end_node=cq.cq_node)
        graph.delete(cq_rel, cq.cq_node)
        # graph.delete(cq.cq_node)

    @staticmethod
    def most_recent_cqs():
        params = {

        }
        cypher_str = ""
        match_results = Graph(settings.DATABASE_URL).cypher.execute(statement=cypher_str,
                                                                    parameters=params)
        cq_list = []
        cq = {}
        for item in match_results:
            cq['id'] = item.id
            cq['subject'] = item.subject
            cq['message'] = item.message
            cq['created_date'] = item.created_date
            cq_list.append(cq)
        root = {}
        root['cqs'] = cq_list
        return root


    def response(self, response_id):
        """
        response dictionary details including user details
        :param response_id:
        :return:  dict with response details and a dict of the user who made the response
        """
        response_node = self._graph_db.find_one(GraphLabel.RESPONSE,
                                               property_key='id',
                                               property_value=response_id)
        response_user_relationship = self._graph_db.match_one(start_node=None,
                                                             rel_type=GraphRelationship.RESPONDED,
                                                             end_node=response_node)
        response_dict = {}
        response_dict['response'] = response_node.auto_sync_properties
        response_dict['user'] = response_user_relationship.start_node.properties
        return response_dict