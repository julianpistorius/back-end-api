from db.location import Location

__author__ = 'Marnee Dearman'
import uuid
import settings
from py2neo import Graph, Node, Relationship

from labels_relationships import GraphRelationship, GraphLabel
from interest import Interest
# from _db.py2neo_user import User


class Organization(object):
    def __init__(self):
        self.name = ''
        self.id = ''
        self.mission_statement = ''
        self.about = ''
        self.is_open = False
        self.is_invite_only = False
        self.is_visible = True
        self.website = ''
        self._graph_db = Graph(settings.DATABASE_URL)

    @property
    def org_node(self):
        return self._graph_db.find_one(GraphLabel.ORGANIZATION,
                                      property_key='id',
                                      property_value=self.id)

    @property
    def org_properties(self):
        properties_dict = dict(self.__dict__)
        del properties_dict['_graph_db']
        return  properties_dict

    @property
    def org_interests(self):
        org_interests = self._graph_db.match(start_node=self.org_node,
                                            rel_type=GraphRelationship.INTERESTED_IN,
                                            end_node=None)
        interests_list = []
        for rel in org_interests:
            interests_list.append(dict(rel.end_node.properties))
        return interests_list

    @property
    def org_locations(self):
        """
        list of locations for the org
        :return: list
        """
        locations = self._graph_db.match(start_node=self.org_node,
                                         rel_type=GraphRelationship.LOCATED_IN,
                                         end_node=None)
        locations_list = []
        for rel in locations:
            locations_list.append(dict(rel.end_node.properties))
        return locations_list

    @property
    def org_members(self):
        """
        list of users.  user is a dictionary of properties
        list of the members of the organization
        :return: list of tuple of member name, email
        """
        org_members_nodes = self._graph_db.match(start_node=self.org_node,
                                                rel_type=GraphRelationship.MEMBER_OF,
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
        new_org_node = Node.cast(GraphLabel.ORGANIZATION, new_org_properties)
        self._graph_db.create(new_org_node)

        return new_org_node

    def add_location(self, location_dict):
        """
        add location relationship to organization
        if location does not exist, create the location node and then create relationship
        :param location_dict:  dictionary object of location to add
        :return:
        """
        location = Location()
        location.id = location_dict['id']
        location_node = location.location_node_by_place_id
        if not location_node:
            location.set_location_properties(location_dict)
            location.create_location()
            location_node = location.location_node_by_place_id
        try:
            self._graph_db.create_unique(self.org_node, GraphRelationship.LOCATED_IN, location_node)
        except:
            pass  #TODO exception handling

    def add_interest(self, interest_id):
        interest = Interest()
        interest.id = interest_id
        interest_node = interest.interest_node_by_id
        org_interest_relationship = Relationship(self.org_node,
                                                 GraphRelationship.INTERESTED_IN,
                                                 interest_node)
        try:
            self._graph_db.create_unique(org_interest_relationship)
        except:
            pass
        return self.org_interests

    def organization_relationships_for_json(self):
        root = {}
        root = dict(self.org_properties)
        root['interests'] = self.org_interests
        root['members'] = self.org_members
        root['locations'] = self.org_locations
        return root