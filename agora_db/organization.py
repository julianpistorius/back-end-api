__author__ = 'Marnee Dearman'
import uuid
import settings
from py2neo import Graph, Node, Relationship

from agora_types import AgoraRelationship, AgoraLabel
from interest import AgoraInterest
# from agora_db.py2neo_user import AgoraUser


class AgoraOrganization(object):
    def __init__(self):
        self.name = ''
        self.id = ''
        self.mission_statement = ''
        self.about = ''
        self.is_open = False
        self.is_invite_only = False
        self.is_visible = True
        self.website = ''
        self.graph_db = Graph(settings.DATABASE_URL)

    @property
    def org_node(self):
        return self.graph_db.find_one(AgoraLabel.ORGANIZATION,
                                      property_key='id',
                                      property_value=self.id)

    @property
    def org_properties(self):
        properties_dict = dict(self.__dict__)
        del properties_dict['graph_db']
        return  properties_dict

    @property
    def org_interests(self):
        org_interests = self.graph_db.match(start_node=self.org_node,
                                            rel_type=AgoraRelationship.INTERESTED_IN,
                                            end_node=None)
        interests_list = []
        for rel in org_interests:
            interests_list.append(dict(rel.end_node.properties))
        return interests_list

    @property
    def org_members(self):
        """
        list of users.  user is a dictionary of properties
        list of the members of the organization
        :return: list of tuple of member name, email
        """
        org_members_nodes = self.graph_db.match(start_node=self.org_node,
                                                rel_type=AgoraRelationship.MEMBER_OF,
                                                end_node=None)
        org_members_list = []
        for rel in org_members_nodes:
            org_members_list.append(dict(rel.end_node.properties))
            # org_members_list.append((item.end_node["name"], item.end_node["email"]))
        return org_members_list

    def set_organization_attributes(self, org_properties):
        for key, value in org_properties.iteritems():
            setattr(self, key, value)

    def get_organization(self):
        org_node = self.org_node
        org_properties = dict(org_node.properties)
        for key, value in org_properties.iteritems():
            setattr(self, key, value)

    def create_organization(self):
        """
        create a new organization
        :return: py2neo Node
        """
        self.id = str(uuid.uuid4())
        new_org_properties = self.org_properties
        new_org_node = Node.cast(AgoraLabel.ORGANIZATION, new_org_properties)
        self.graph_db.create(new_org_node)

        return new_org_node

    def add_interest(self, interest_id):
        interest = AgoraInterest()
        interest.id = interest_id
        interest_node = interest.interest_node_by_id
        org_interest_relationship = Relationship(self.org_node,
                                                 AgoraRelationship.INTERESTED_IN,
                                                 interest_node)
        try:
            self.graph_db.create_unique(org_interest_relationship)
        except:
            pass
        return self.org_interests

    def organization_relationships_for_json(self):
        root = {}
        root = dict(self.org_properties)
        root['interests'] = self.org_interests
        root['members'] = self.org_members
        return root