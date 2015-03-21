__author__ = 'marnee'

import uuid
import datetime
import sys
import settings
from py2neo import Node, Graph, Relationship, Path, Rev
from labels_relationships import GraphRelationship, GraphLabel


class Conversation(object):
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
    def conversation_properties(self):
        """

        :return:
        """
        properties_dict = dict(self.__dict__)
        del properties_dict['graph_db']
        return properties_dict

    @property
    def conversation_node(self):
        """

        :return:
        """
        if self.id != '':
            return self.graph_db.find_one(GraphLabel.CONVERSATION,
                                          property_key='id',
                                          property_value=self.id)

    @property
    def response_list(self):
        """
        list of responses to this conversation
        :return:
        """
        convo_response_relationship = self.graph_db.match(start_node=None,
                                                          rel_type=GraphRelationship.TO,
                                                          end_node=self.conversation_node)
        response_list = []
        for rel in convo_response_relationship:
            response = rel.start_node.properties
            response_list.append(response)
        return response_list

    @property
    def started_by(self):
        """
        who started this conversation
        :return:
        """
        convo_starter_relationship = self.graph_db.match_one(start_node=None,
                                                         rel_type=GraphRelationship.STARTED,
                                                         end_node=self.conversation_node)
        if convo_starter_relationship:
            return convo_starter_relationship.start_node.properties

    @property
    def started_with(self):
        """

        :return:
        """
        convo_with_relationship = self.graph_db.match_one(start_node=self.conversation_node,
                                                          rel_type=GraphRelationship.WITH,
                                                          end_node=None)
        if convo_with_relationship:
            return convo_with_relationship.end_node.properties



    def create_response(self, user_id, message):
        new_convo_response = Node.cast(GraphLabel.RESPONSE,
                                       id=str(uuid.uuid4()),
                                       created_date=datetime.datetime.now(),
                                       message=message)
        try:
            self.graph_db.create(new_convo_response)
            response_node = self.graph_db.find_one(GraphLabel.RESPONSE,
                                                   property_key='id',
                                                   property_value=id)

            response_convo_relationship = Relationship(response_node,
                                                       GraphRelationship.TO,
                                                       self.conversation_node)
            self.graph_db.create(response_convo_relationship)
        except:
            pass  #TODO exception handling

    def get_conversation_users(self):
        """
        a dictionary of the users the conversation is between
        :return:
        """
        rel_types = []
        rel_types.append(GraphRelationship.STARTED)
        rel_types.append(GraphRelationship.CREATED)
        between_relationship = self.graph_db.match(start_node=self.conversation_node,
                                                   rel_type=rel_types,
                                                   end_node=None,
                                                   bidirectional=True)
        convo_user = {}
        users = []
        if between_relationship:
            for rel in between_relationship:
                convo_user['id'] = rel.end_node.properties['id']
                convo_user['name'] = rel.end_node.properties['name']
                convo_user['call_sign'] = rel.end_node.properties['call_sign']
                users.append(convo_user)
        return users

    def get_responses(self):
        """

        :return:
        """

    def conversation_for_json(self):
        root = {}
        root = self.conversation_properties
        root['users'] = self.get_conversation_users()
        return root