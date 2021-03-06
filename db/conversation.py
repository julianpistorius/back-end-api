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
        self._graph_db = Graph(settings.DATABASE_URL)

    @property
    def conversation_properties(self):
        """

        :return:
        """
        properties_dict = dict(self.__dict__)
        del properties_dict['_graph_db']
        return properties_dict

    @property
    def conversation_node(self):
        """

        :return:
        """
        if self.id != '':
            return self._graph_db.find_one(GraphLabel.CONVERSATION,
                                          property_key='id',
                                          property_value=self.id)

    @property
    def response_list(self):
        """
        list of responses to this conversation
        :return:
        """
        convo_response_relationship = self._graph_db.match(start_node=None,
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
        convo_starter_relationship = self._graph_db.match_one(start_node=None,
                                                         rel_type=GraphRelationship.STARTED,
                                                         end_node=self.conversation_node)
        if convo_starter_relationship:
            return convo_starter_relationship.start_node.properties

    @property
    def started_with(self):
        """

        :return:
        """
        convo_with_relationship = self._graph_db.match_one(start_node=self.conversation_node,
                                                          rel_type=GraphRelationship.WITH,
                                                          end_node=None)
        if convo_with_relationship:
            return convo_with_relationship.end_node.properties

    def set_conversation_properties(self, conversation_properties):
        """
        set conversation properties
        :param conversation_properties:
        :return:
        """
        for key, value in conversation_properties.iteritems():
            setattr(self, key, value)

    def update_conversation(self):
        """

        :return:
        """
        convo = self._graph_db.find_one(GraphLabel.CONVERSATION,
                                       property_key='id',
                                       property_value=self.id)
        convo.properties = self.conversation_properties
        convo.push()

    def create_response(self, user_id, message):
        new_convo_response = Node.cast(GraphLabel.RESPONSE,
                                       id=str(uuid.uuid4()),
                                       created_date=datetime.datetime.now(),
                                       message=message)
        try:
            self._graph_db.create(new_convo_response)
            response_node = self._graph_db.find_one(GraphLabel.RESPONSE,
                                                   property_key='id',
                                                   property_value=id)

            response_convo_relationship = Relationship(response_node,
                                                       GraphRelationship.TO,
                                                       self.conversation_node)
            self._graph_db.create(response_convo_relationship)
        except:
            pass  #TODO exception handling

    def get_conversation_users(self):
        """
        a dictionary of the users the conversation is between
        :return:
        """
        rel_types = []
        rel_types.append(GraphRelationship.STARTED)
        rel_types.append(GraphRelationship.WITH)
        between_relationship = self._graph_db.match(start_node=self.conversation_node,
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
        # rel_types = []
        # rel_types.append(GraphRelationship.RESPONDED)
        # rel_types.append(GraphRelationship.TO)
        responses_relationship = self._graph_db.match(start_node=None,
                                                     rel_type=GraphRelationship.TO,
                                                     end_node=self.conversation_node)
        responses = []
        for rel in responses_relationship:
            response_node = rel.start_node
            response_from = self._graph_db.match_one(start_node=None,
                                                    rel_type=GraphRelationship.RESPONDED,
                                                    end_node=response_node)
            response_properties = response_node.properties
            response_properties['by'] = '%s / %s' % (response_from.start_node.properties['name'],
                                                    response_from.start_node.properties['call_sign'])
            responses.append(response_properties)
        return responses

    def conversation_for_json(self):
        root = {}
        root = self.conversation_properties
        root['users'] = self.get_conversation_users()
        root['responses'] = self.get_responses()
        return root