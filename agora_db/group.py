

__author__ = 'Marnee Dearman'
import uuid
import settings
from py2neo import Graph, Node, Relationship
from interest import AgoraInterest
from location import AgoraLocation
from conversation import AgoraConversation
# from py2neo_user import AgoraUser
from agora_types import AgoraRelationship, AgoraLabel
# from agora_db.user import AgoraUser


class AgoraGroup(object):
    def __init__(self):
        self.name = ''
        self.id = None
        self.about = ''
        self.mission_statement = ''
        self.is_open = None
        self.is_invite_only = False
        self.last_updated_date = ''
        # self.meeting_location = ''
        # self.next_meeting_date = None
        # self.next_meeting_time = None
        # self.creator = '' #by id
        # self.moderators = [] #by id  #TODO change this to a relationship in the graph
        self.website = ''
        self.graph_db = Graph(settings.DATABASE_URL)

    @property
    def group_properties(self):
        properties_dict = dict(self.__dict__)
        del properties_dict['graph_db']
        return properties_dict

    def set_group_properties(self, group_properties):
        for key, value in group_properties.iteritems():
            setattr(self, key, value)

    def get_group(self):
        """
        get the group info (attributes) based on the id
        :return:
        """
        group_node = self.group_node
        group_properties = dict(group_node.properties)
        if not group_node is None:
            for key, value in group_properties.iteritems():
                setattr(self, key, value)

    @property
    def group_node(self):
        """
        get a group node based on the unique id attribute
        :return: neo4j.Node
        """
        return self.graph_db.find_one(AgoraLabel.STUDYGROUP,
                                      property_key='id',
                                      property_value=self.id)

    @property
    def group_interests(self):
        """ get user interests
        :return: list of interests
        """
        group_interests = self.graph_db.match(start_node=self.group_node,
                                              rel_type=AgoraRelationship.INTERESTED_IN,
                                              end_node=None)
        # create a list of tuples of interests and the users's relationship to them
        interests_list = []
        for rel in group_interests:
            interest = AgoraInterest()
            interest.id = rel.end_node['id']
            interest.get_interest_by_id()
            interest_dict = {}
            interest_dict = interest.interest_properties
            interests_list.append(interest_dict)
            # interests_list.append((item.end_node["name"], item["description"]))
        # return [item.end_node["name"] for item in user_interests]
        return interests_list

    @property
    def group_locations(self):
        """

        :return: list of locations
        """
        group_locations = self.graph_db.match(start_node=self.group_node,
                                              rel_type=AgoraRelationship.LOCATED_IN,
                                              end_node=None)
        locations_list = []
        for rel in group_locations:
            location_dict = {}
            location = AgoraLocation()
            location.id = rel.end_node['id']
            location_dict = dict(location.location_properties)
            locations_list.append(location_dict)
            # locations_list.append(item.end_node["formatted_address"])
        return locations_list

    @property
    def group_members(self):
        group_member_nodes = self.graph_db.match(start_node=self.group_node,
                                            rel_type=AgoraRelationship.MEMBER_OF,
                                            end_node=None)
        members_list = []
        for rel in group_member_nodes:
            member_dict = {}
            # member = AgoraUser()
            # member.id = rel.end_node['id']
            # member_dict = dict(rel.end_node.properties)
            members_list.append(dict(rel.end_node.properties))
            # members_list.append((member_node.end_node["name"], member_node.end_node["id"]))
        return members_list

    @property
    def group_creator(self):
        """

        :return: dictionary object with creator user information
        """
        group_creator = self.graph_db.match(start_node=self.group_node,
                                                 rel_type=AgoraRelationship.CREATED,
                                                 end_node=None)
        creator_dict = {}
        for rel in group_creator:
            creator_dict = dict(rel.end_node.properties)
        return creator_dict

    @property
    def group_moderators(self):
        """

        :return: list of user dictionary objects where the users are moderators
        """
        group_moderators = self.graph_db.match(start_node=self.group_node,
                                               rel_type=AgoraRelationship.MODERATES,
                                               end_node=None)
        moderators_list = []
        for rel in group_moderators:
            moderators_list.append(dict(rel.end_node.properties))
        return moderators_list


    def create_group(self):
        """
        create new study group or circle
        :return: py2neo Node
        """
        self.id = str(uuid.uuid4())

        new_group_node = Node.cast(AgoraLabel.STUDYGROUP, self.group_properties)
        try:
            self.graph_db.create(new_group_node)
        except:
            pass

        return new_group_node

    def add_interest(self, interest_id):
        """
        link interests to a study group
        :return: list of group interests
        """
        #TODO exception handling
        interest = AgoraInterest()
        interest.id = interest_id
        group_interest_relationship = Relationship(interest.interest_node_by_id,
                                                   AgoraRelationship.INTERESTED_IN,
                                                   self.group_node)
        try:
            self.graph_db.create(group_interest_relationship)
        except:
            pass

        #TODO set properties on RELATIONSHIP
        return self.group_interests

    def update_group(self):
        group_node = self.group_node
        for key in self.group_properties.keys():
            group_node[key] = self.group_properties[key]
        group_node.push()

    def allow_edit(self, auth_key):
        """

        :return:
        """
        allow = False
        moderators = self.group_moderators
        creator = self.group_creator
        if auth_key == creator['id']:
            allow = True
        else:
            for mod in moderators:
                if auth_key == mod['id']:
                    allow = True
        return allow

    #TODO close group
    def close_group(self):
        pass

    def matched_groups(self, match_string, limit):
        """
        get a set of groups by name by
        :param match_string:  partial name of group to search by
        :param limit:  number of records to return in result set
        :return: dictionary of search results
        """
        params = {
            'match': '(?i)%s.*' % match_string,
            'limit': limit
        }
        cypher_str = "MATCH (group:STUDYGROUP ) " \
            "WHERE group.name =~ {match} " \
            "RETURN group.name as name, group.id as id " \
            "LIMIT {limit}"
        match_results = self.graph_db.cypher.execute(statement=cypher_str, parameters=params)
        root = {}
        root['count'] = 0
        group_found = {}
        groups_list = []
        for item in match_results:
            group_found['id'] = item.id
            group_found['name'] = item.name
            # self.id = item['id']
            # self.get_user()
            # users_list.append(dict(self.user_properties))
            groups_list.append(dict(group_found))
            root['count'] += 1
        root['groups'] = groups_list
        return root

    def add_conversation(self, subject, message):
        convo = AgoraConversation()
        convo.subject = subject
        convo.message = message
        convo.create_conversation_for_group(self.id)

    def update_conversation(self, subject, message, convo_id):
        pass  #TODO add update conversation

    def group_for_json(self):
        # self
        # root = {}
        # root['id'] = self.id
        # root['name'] = self.name
        # root['description'] = self.description
        # root['is_invite_only'] = self.is_invite_only
        # root['is_open'] = self.is_open
        # root['meeting_location'] = self.meeting_location
        # root['next_meeting_date'] = self.next_meeting_date
        # root['next_meeting_time'] = self.next_meeting_time
        # root['interests'] = self.group_interests
        # root['users'] = self.group_members
        # # root['locations'] = self.group_locations
        return self.group_properties



