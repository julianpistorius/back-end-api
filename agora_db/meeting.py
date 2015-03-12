__author__ = 'marnee'
import uuid
import datetime
import sys
import settings
from py2neo import Node, Graph, Relationship, Path, Rev
from interest import AgoraInterest
from goal import AgoraGoal
from group import AgoraGroup
from location import AgoraLocation
from organization import AgoraOrganization
from agora_types import AgoraRelationship, AgoraLabel

#TODO exception handling


class AgoraMeeting(object):
    def __init__(self):
        """

        :return:
        """
        self.id = ''
        self.name = ''
        self.description = ''
        self.where = ''
        self.date = ''
        self.time = ''
        self.created_date = ''
        self.is_recurring = False
        self.graph_db = Graph(settings.DATABASE_URL)

    @property
    def meeting_properties(self):
        """

        :return:
        """
        properties_dict = dict(self.__dict__)
        del properties_dict['graph_db']
        return properties_dict

    @property
    def meeting_node(self):
        """

        :return:
        """
        if self.id != '':
            return self.graph_db.find_one(AgoraLabel.MEETING,
                                          property_key='id',
                                          property_value=self.id)

    @property
    def group(self):
        """

        :return: AgoraGroup() that is attached to this meeting
        """
        meeting_group_relationship = self.graph_db.match(start_node=None,
                                                         rel_type=AgoraRelationship.HAS_MEETING,
                                                         end_node=self.meeting_node)
        group = AgoraGroup()
        for rel in meeting_group_relationship:
            group.id = rel.end_node.properties['id']
            group.get_group()
        return group

    def set_meeting_properties(self, meeting_properties):
        """

        :param meeting_properties:
        :return:
        """
        for key, value in meeting_properties.iteritems():
            setattr(self, key, value)

    # @staticmethod
    def get_meeting(self):
        """

        :return:
        """
        meeting_node = self.meeting_node
        if meeting_node is not None:
            meeting_properties = dict(meeting_node.properties)
            for key, value in meeting_properties.iteritems():
                setattr(self, key, value)

    def create_meeting(self, meeting_properties=None):
        """

        :param meeting_properties:
        :return:
        """
        self.created_date = datetime.date.today()
        self.id = str(uuid.uuid4())
        if meeting_properties is not None:
            self.set_meeting_properties(meeting_properties)
        new_meeting_node = Node.cast(AgoraLabel.MEETING, self.meeting_properties)
        try:
            self.graph_db.create(new_meeting_node)
        except:
            pass
        return new_meeting_node

    def update_meeting(self):
        """

        :return:
        """
        meeting_node = self.meeting_node
        meeting_properties = dict(self.meeting_properties)
        for key, value in meeting_properties.iteritems():
            meeting_node[key] = value
        meeting_node.push()

    @property
    def attendees(self):
        """

        :return: list of attendees dictionaries.  these are the users who are attending the meeting
        """
        #TODO get attendees
        return []

    def allow_edit(self, auth_key):
        """
        check if the user is a creator or moderator for the group attached to the meeting
        :param auth_key:
        :return:
        """
        allow = False
        group = self.group
        moderators = group.group_moderators
        creator = dict(group.group_creator)
        if auth_key == creator['id']:
            allow = True
        else:
            for mod in moderators:
                if auth_key == mod['id']:
                    allow = True
        return allow

    def meeting_for_json(self, auth_key):
        root = dict(self.meeting_properties)
        root['groups'] = dict(self.group.group_properties)
        root['attendees'] = self.attendees
        root['allow_edit'] = self.allow_edit(auth_key=auth_key)
        return root