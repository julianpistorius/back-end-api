__author__ = 'marnee'

import uuid
import datetime
import sys
import settings
from py2neo import Node, Graph, Relationship, Path, Rev
from agora_types import AgoraRelationship, AgoraLabel
from agora_db.user import AgoraUser
from agora_db.group import AgoraGroup


class AgoraConversation(object):
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
            return self.graph_db.find_one(AgoraLabel.CONVERSATION,
                                          property_key='id',
                                          property_value=self.id)

    @property
    def response_list(self):
        """
        list of responses to this conversation
        :return:
        """
        convo_response_relationship = self.graph_db.match(start_node=None,
                                                          rel_type=AgoraRelationship.TO,
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
                                                         rel_type=AgoraRelationship.STARTED,
                                                         end_node=self.conversation_node)
        if convo_starter_relationship:
            return convo_starter_relationship.start_node.properties

    @property
    def started_with(self):
        """

        :return:
        """
        convo_with_relationship = self.graph_db.match_one(start_node=self.conversation_node,
                                                          rel_type=AgoraRelationship.WITH,
                                                          end_node=None)
        if convo_with_relationship:
            return convo_with_relationship.end_node.properties

    def create_converation_between_users(self, user_id_started, user_id_with):
        self.id = uuid.uuid4()
        new_convo_node = Node.cast(AgoraLabel.CONVERSATION, self.conversation_properties)
        try:
            self.graph_db.create(new_convo_node)  # create new conversation node
            user_started = AgoraUser()
            user_started.id = user_id_started
            user_with = AgoraUser()
            user_with.id = user_id_with
            # create started conversation relationship
            user_started_relationship = Relationship(user_started.user_node,
                                                     AgoraRelationship.STARTED,
                                                     self.conversation_node)
            self.graph_db.create(user_started_relationship)
            # create started conversation with relationship
            convo_with_relationship = Relationship(self.conversation_node,
                                                   AgoraRelationship.WITH,
                                                   user_with.user_node)
            self.graph_db.create(convo_with_relationship)
            # return new_convo_node
        except:
            pass  #TODO add exception handling

    def create_conversation_for_group(self, group_id):
        self.id = str(uuid.uuid4())
        self.created_date = datetime.date.today()
        new_group_convo = Node.cast(AgoraLabel.CONVERSATION, self.conversation_properties)
        try:
            self.graph_db.create(new_group_convo)
            group = AgoraGroup()
            group.id = group_id
            # create group started relationship
            group_convo_relationship = Relationship(group.group_node,
                                                    AgoraRelationship.STARTED,
                                                    self.conversation_node)
            self.graph_db.create(group_convo_relationship)
        except:
            pass  #TODO add exception handling

    def create_response(self, user_id, message):
        new_convo_response = Node.cast(AgoraLabel.RESPONSE,
                                       id=str(uuid.uuid4()),
                                       created_date=datetime.datetime.now(),
                                       message=message)
        try:
            self.graph_db.create(new_convo_response)
            response_node = self.graph_db.find_one(AgoraLabel.RESPONSE,
                                                   property_key='id',
                                                   property_value=id)

            response_convo_relationship = Relationship(response_node,
                                                       AgoraRelationship.TO,
                                                       self.conversation_node)
            self.graph_db.create(response_convo_relationship)
        except:
            pass  #TODO exception handling