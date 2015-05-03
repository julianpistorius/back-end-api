_author__ = 'Marnee Dearman'
import uuid
import datetime
import sys
import settings
from py2neo import Node, Graph, Relationship, Path, Rev
from interest import Interest
from goal import Goal
from group import Group
from location import Location
from organization import Organization
from cq import Cq
from labels_relationships import GraphRelationship, GraphLabel
from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer, BadSignature, BadTimeSignature
from services import notifications


class User(object):
    def __init__(self, graph_db=None):
        self.name = ''
        self.call_sign = ''
        self.first_name = ''
        self.last_name = ''
        self.id = ''
        self.mission_statement = ''
        self.about = ''
        self.email = ''
        self.is_mentor = False
        self.is_tutor = False
        self.is_visible = True
        self.is_available_for_in_person = True
        # self._interests_list = None
        # self.is_admin = False
        # self.password = ''
        # self.salt = ''
        # self.permanent_web_token = ''
        # self.temporary_web_token = ''
        self.join_date = None
        self.last_active_date = ''
        self._graph_db = Graph(settings.DATABASE_URL)

    @property
    def user_properties(self):
        """
        setup user properties
        :return: dictionary of properties
        """
        properties_dict = dict(self.__dict__)
        del properties_dict['_graph_db']
        return properties_dict

    def set_user_properties(self, user_properties):
        """

        :param user_properties:
        :return:
        """
        for key, value in user_properties.iteritems():
            setattr(self, key, value)

    def get_user(self):
        """

        :return:
        """
        user_node = self.user_node
        if user_node is not None:
            user_properties = dict(user_node.properties)
            for key, value in user_properties.iteritems():
                setattr(self, key, value)
            return user_node
        else:
            return None

    def create_user(self, user_properties=None):
        """
        create a new user based on the attributes
        :return: node
        """
        #TODO exception handling
        self.join_date = datetime.date.today()
        self.last_active_date = self.join_date
        self.id = str(uuid.uuid4())
        if user_properties is not None:
            self.set_user_properties(user_properties)
        new_user_node = Node.cast(GraphLabel.USER, self.user_properties)
        try:
            self._graph_db.create(new_user_node)
        except:
            pass
            # print 'node probably found.  see message'
            # print sys.exc_info()
        return new_user_node

    @property
    def user_node(self):
        """
        get a user Node
        :return: py2neo Node
        """
        if self.email != '':
            return self._graph_db.find_one(GraphLabel.USER,
                                          property_key='email',
                                          property_value=self.email)
        elif self.id != '':
            return self._graph_db.find_one(GraphLabel.USER,
                                          property_key='id',
                                          property_value=self.id)

        # return self.graph_db.get_or_create_indexed_node(index_name=GraphLabel.USER,
        #                                                      key='email', value=self.email)

    @property
    def user_cqs(self):
        """
        get list of cqs for the user
        :return: list of cqs
        """
        user_cqs = self._graph_db.match(start_node=self.user_node,
                                        rel_type=GraphRelationship.SENT,
                                        end_node=None)
        cqs_list = []
        for rel in user_cqs:
            cqs_list.append(dict(rel.end_node.properties))
        return cqs_list

    @property
    def user_interests(self):
        """ get user interests
        :return: dictionary of interests
        """
        user_interests = self._graph_db.match(start_node=self.user_node,
                                             rel_type=GraphRelationship.INTERESTED_IN,
                                             end_node=None)
        #create a list of tuples of interests and the users's relationship to them

        interests_list = []
        for rel in user_interests:
            interest_dict = dict(rel.end_node.properties, **rel.properties)
            interests_list.append(dict(rel.end_node.properties))
        return interests_list

    @property
    def user_goals(self):
        """ get user interests
        :return: list of interests
        """
        #TODO do not need a list of interests -- HATEOAS -- MMD 3/8/2015
        user_goals = self._graph_db.match(start_node=self.user_node, rel_type=GraphRelationship.HAS_GOAL,
                                         end_node=None)
        goals_list = []
        goal_interests_list = []
        for rel in user_goals:
            goal_properties = dict(rel.end_node.properties)
            goal = Goal()
            goal.id = goal_properties['id']
            interests = goal.goal_interests
            interests_list = []
            for interest in interests:
                interests_list.append(interest['name'])
            goal_properties['interests'] = interests_list
            goals_list.append(goal_properties)

        return goals_list

    @property
    def user_groups(self):
        """

        :return: list of tuples of the groups
        """
        #TODO add list of related interests
        user_groups = self._graph_db.match(start_node=self.user_node, rel_type=GraphRelationship.STUDIES_WITH,
                                          end_node=None)
        # create a list of tuples of interests and the users's relationship to them
        groups_list = []
        for rel in user_groups:
            group_properties = dict(rel.end_node.properties)
            group = Group()
            group.id = group_properties['id']
            interests = group.group_interests
            group_interests_list = []
            for interest in interests:
                group_interests_list.append(interest['name'])
            group_properties['interests'] = group_interests_list
            groups_list.append(group_properties)
        return groups_list

    @property
    def user_orgs(self):
        """

        :return:
        """
        user_orgs = self._graph_db.match(start_node=self.user_node,
                                        rel_type=GraphRelationship.MEMBER_OF,
                                        end_node=None)
        orgs_list = []
        for rel in user_orgs:
            org_properties = dict(rel.end_node.properties)
            org = Organization()
            org.id = org_properties['id']
            interests = org.org_interests
            interests_list = []
            for interest in interests:
                interests_list.append(interest['name'])
            org_properties['interests'] = interests_list
            orgs_list.append(org_properties)
        return orgs_list

    @property
    def user_locations(self):
        """

        :return:
        """
        user_locations = self._graph_db.match(start_node=self.user_node,
                                        rel_type=GraphRelationship.LOCATED_IN,
                                        end_node=None)

        locations_list = []
        for rel in user_locations:
            locations_list.append(rel.end_node.properties)
        return locations_list

    def get_local_users_shared_interests_near_location(self):   #, location_node):
        """
        get a dictionary of user with shared interests with this user
        :param :
        :return:  dictionary of {interests: [users]}
        """
        # users_shared_interests
        params = {
            'email': 'marnee@society.com'
        }
        cypher_str = "MATCH (u:USER {email:{email}})-[url:LOCATED_IN]->(l:LOCATION)"
        cypher_str += "<-[orl:LOCATED_IN]-(o:USER) "
        cypher_str += "WITH u, o, l, url, orl "
        cypher_str += "MATCH (u)-[ru:INTERESTED_IN]->"
        cypher_str += "(i:INTEREST)<-[ro:INTERESTED_IN]-(o) "
        cypher_str += "RETURN i.name as interest_name, i.id as interest_id, " \
                      "o.name as user_name, o.id as user_id" #, u, ru, ro, l, url, orl"
        # print cypher_str
        results = Graph().cypher.execute(cypher_str, params)
        # self.graph_db.cypher.stream(cypher_str)
        # self.graph_db.cypher.execute(cypher_str)
        interest_users_dict = {}
        print results
        for item in results:
            interest = item['interest_name']
            user = item['user_name']
            if interest_users_dict.has_key(interest):
                interest_users_dict[interest].append(user)
            else:
                interest_users_dict[interest] = []
                interest_users_dict[interest].append(user)
            # user = item['user_name']
            # cur_users_list.append(interest_users_dict.get(interest))
            # if interest_users_dict.has_key(interest):
            # # if interest in interest_users_dict.keys():
            #     cur_users_list = interest_users_dict[interest]
            #     # cur_users_list = interest_users_dict.get(interest)
            # else:
            #     interest_users_dict[interest] = []
            # cur_users_list.append(user)
            # interest_users_dict[interest] = cur_users_list
            # interest_users_dict[interest] = interest_users_dict.get(interest)
            # user_details = (user_node['name'], user_node['email'], user_node['id'])
            # user_list.append(user_details)
        return interest_users_dict

    def add_interest(self, interest_id, experience_properties_dict=None):
        """ Add interest to user
        :param interest id:string uuid
        :return: List of interests
        """
        #TODO add exception handling
        interest = Interest()
        interest.id = interest_id
        interest_node = interest.interest_node_by_id
        user_interest_relationship = Relationship(self.user_node,
                                                  GraphRelationship.INTERESTED_IN,
                                                  interest_node)
        for key, value in experience_properties_dict.iteritems():
            user_interest_relationship[key] = value
        try:
            self._graph_db.create_unique(user_interest_relationship)
        except:
            pass
        return self.user_interests

    def update_interest(self, interest_id, experience_properties_dict):
        interest = Interest()
        interest.id = interest_id
        interest_node = interest.interest_node_by_id
        user_interest_relationship = self._graph_db.match_one(start_node=self.user_node,
                                                             rel_type=GraphRelationship.INTERESTED_IN,
                                                             end_node=interest_node)
        for key, value in experience_properties_dict.iteritems():
            user_interest_relationship.properties[key] = value
        user_interest_relationship.push()

    def delete_interest(self, interest_id):
        """
        drop interest relationship from user given the interest_id
        :param interest_id: str(uuid.uuid4())
        :return:
        """
        #TODO exception handling
        interest = Interest()
        interest.id = interest_id
        interest_node = interest.interest_node_by_id
        user_interest_relationship = self._graph_db.match_one(start_node=self.user_node,
                                                             rel_type=GraphRelationship.INTERESTED_IN,
                                                             end_node=interest_node)
        self._graph_db.delete(user_interest_relationship)

    def update_user(self):
        user_node = self.user_node
        user_properties = dict(self.user_properties)
        for key, value in user_properties.iteritems():
            user_node[key] = value  # user_properties[key]
        user_node.push()

    # def make_admin(self):
    #     #new_user = self.graph_db.get_or_create_indexed_node(index_name=GraphLabel.USER, key='email', value=self.email)
    #     self.user_node.add_labels(GraphLabel.ADMIN)

    def add_goal(self, goal_properties):
        """
        Add goal to user
        :param goal_id: string uuid
        :return: List of user goals
        """
        #TODO exception handling
        goal = Goal()
        goal.set_goal_properties(goal_properties=goal_properties)
        goal.create_goal()
        # create relationship between user and interest node
        user_goal_relationship = Relationship(self.user_node,
                                              GraphRelationship.HAS_GOAL,
                                              goal.goal_node)

        self._graph_db.create_unique(user_goal_relationship)
        #TODO set properties on the relationship -- may use a unique id as the key
        return self.user_goals

    def delete_goal(self, goal_id):
        user_node = self.user_node
        goal = Goal()
        goal.id = goal_id
        # have to remove all relationships before deleteing a node
        goal.delete_all_interests()
        goal_node = goal.goal_node
        user_goal_rel = self._graph_db.match_one(start_node=user_node,
                                                rel_type=GraphRelationship.HAS_GOAL,
                                                end_node=goal_node)
        self._graph_db.delete(user_goal_rel)
        self._graph_db.delete(goal_node)

    def join_group(self, group_id, group_relationship_properties=None):
        """
        Add user as member of group
        :param group_id: string uuid
        :return:
        """
        #TODO exception handling
        group = Group()
        group.id = group_id
        # relationship properties
        join_properties = {
            'join_date': datetime.date.today()
        }
        user_group_relationship = Relationship(self.user_node,
                                               GraphRelationship.STUDIES_WITH,
                                               group.group_node)
                                               # properties=join_properties)
        for key, value in join_properties.iteritems():
            user_group_relationship[key] = value
        try:
            self._graph_db.create_unique(user_group_relationship)
        except:
            pass
        #TODO set properties on the relationsip
        # group_relationship_properties["id"] = str(uuid.uuid4())

    def leave_group(self, group_id):
        """
        remove relationship between user and study group
        :param group_id: string uuid
        :return: None
        """
        #TODO exception handling
        group = Group()
        group.id = group_id
        user_group_relationship = self._graph_db.match_one(start_node=self.user_node,
                                                          rel_type=GraphRelationship.MEMBER_OF,
                                                          end_node=group.group_node)

        self._graph_db.delete(user_group_relationship)

    def delete_group(self, group_id):
        pass

    def join_organization(self, organization_id):
        """
        add user to organization
        :param organization_id: string uuid
        :return: list of tuple of interests
        """
        #TODO exception handling
        org = Organization()
        org.id = organization_id

        user_org_relationship = Relationship(self.user_node,
                                             GraphRelationship.MEMBER_OF,
                                             org.org_node)
        try:
            self._graph_db.create_unique(user_org_relationship)
        except:
            print sys.exc_info()[0]

    def leave_organization(self, organization_id):
        """
        remove relationship between user and organization
        :param organization_id:
        :return:
        """
        #TODO exception handling
        org = Organization()
        org.id = organization_id
        user_org_relationship = self._graph_db.match_one(start_node=self.user_node,
                                                        rel_type=GraphRelationship.MEMBER_OF,
                                                        end_node=org.org_node)
        self._graph_db.delete(user_org_relationship)

    def add_location(self, location_json):
        """
        link user to location nodes
        :param locations_place_id:
        :return:
        """
        #TODO exception handling
        #TODO do in location and pass in the node from the actual object (better pattern)
        location_place_id = location_json['id']
        location = Location()
        location.id = location_place_id
        location_node = location.location_node_by_place_id
        if not location_node:
            location.set_location_properties(location_json)
            location.create_location()
            location_node = location.location_node_by_place_id()

        user_location_relationship = Relationship(self.user_node,
                                                  GraphRelationship.LOCATED_IN,
                                                  location_node)
        # try:
        self._graph_db.create_unique(user_location_relationship)
        # except:
        #     pass

    def create_cq(self, cq_dict, cq_interests_dict=None):
        cq_node = Cq.create_cq(user_node=self.user_node, cq_dict=cq_dict, cq_interests_dict=cq_interests_dict)
        return cq_node

    def update_cq(self, cq_dict, cq_interests_dict=None):
        # cq_node =
        #TODO:  update cq, see TODO on cq class
        pass


    def create_converation_between_users(self, user_id_started, user_id_with, conversation_properties):
        # self.id = uuid.uuid4()
        conversation_properties['id'] = str(uuid.uuid4())
        new_convo_node = Node.cast(GraphLabel.CONVERSATION, conversation_properties)
        try:
            convo_node, = self._graph_db.create(new_convo_node)  # create new conversation node
            user_started = User()
            user_started.id = user_id_started
            user_with = User()
            user_with.id = user_id_with
            # create started conversation relationship
            user_started_relationship = Relationship(user_started.user_node,
                                                     GraphRelationship.STARTED,
                                                     convo_node)
            self._graph_db.create(user_started_relationship)
            # create started conversation with relationship
            convo_with_relationship = Relationship(convo_node,
                                                   GraphRelationship.WITH,
                                                   user_with.user_node)
            self._graph_db.create(convo_with_relationship)
            return convo_node.properties['id']
        except:
            pass  #TODO add exception handling


    # @staticmethod
    def matched_users(self, match_string, limit):
        """

        :param match_string:
        :param limit:
        :return: dictionary of search results
        """
        params = {
            'match': '(?i)%s.*' % match_string,
            'limit': limit
        }
        cypher_str = "MATCH (user:USER ) " \
            "WHERE user.name =~ {match} " \
            "RETURN user.name as name, user.id as id " \
            "LIMIT {limit}"
        match_results = self._graph_db.cypher.execute(statement=cypher_str, parameters=params)
        root = {}
        root['count'] = 0
        user_found = {}
        users_list = []
        for item in match_results:
            user_found['id'] = item.id
            user_found['name'] = item.name
            # self.id = item['id']
            # self.get_user()
            # users_list.append(dict(self.user_properties))
            users_list.append(dict(user_found))
            root['count'] += 1
        root['users'] = users_list
        return root

    @staticmethod
    def register_user(email):
        verification_email = notifications.Notifications()
        verification_email.recipients = [email]
        s = URLSafeTimedSerializer(secret_key=settings.TOKEN_SECRET_KEY)
        payload = s.dumps(email)
        verification_email.subject = settings.ACTIVATION_SUBJECT
        verification_email.message = settings.ACTIVATION_MESSAGE
        verification_email.url = User.construct_verification_url(payload=payload)
        verification_email.send_by_gmail()

    def activate_user(self, payload, email):
        s = URLSafeTimedSerializer(secret_key=settings.TOKEN_SECRET_KEY)
        payload_email = s.loads(payload, max_age=settings.TOKEN_EXPIRES_IN)  # 10 minutes
        if email == payload_email:
            self.email = email
            self.get_user()
            self.permanent_web_token = User.create_web_token(self.id)
            if self.id == '':
                self.create_user()
            else:
                self.update_user()
        else:
            raise BadSignature('bad email')

    def update_last_active_date(self):
        self.last_active_date = datetime.date.today()
        user_node = self.user_node
        user_node['last_active_date'] = self.last_active_date
        user_node.push()

    @staticmethod
    def construct_verification_url( payload):
        return settings.SITE_URL + settings.ACTIVATION_ROUTE + "/%s" % payload

    @staticmethod
    def create_web_token(id):
        s = URLSafeSerializer(secret_key=settings.TOKEN_SECRET_KEY)
        return s.dumps(id)

    def user_relationships_for_json(self, auth_id):
        root = self.user_profile_for_json()
        root['__class'] = self.__class__.__name__
        root['interests'] = self.user_interests
        root['locations'] = self.user_locations
        root['goals'] = self.user_goals
        root['groups'] = self.user_groups
        root['organizations'] = self.user_orgs
        root['is_owner'] = (auth_id == self.id)
        root['allow_edit'] = (auth_id == self.id)
        root['allow_message'] = (auth_id is not None)
        return root

    def user_profile_for_json(self):
        root = self.user_properties
        return root

    def user_cqs_for_json(self):
        root = {}
        root['__class'] = self.__class__.__name__
        root['id'] = self.id
        root['email'] = self.email
        root['cqs'] = self.user_cqs


    def user_interests_for_json(self):
        root = {}
        root['__class'] = self.__class__.__name__
        root['id'] = self.id
        root['email'] = self.email
        root['interests'] = self.user_interests
        return root

    def user_goals_for_json(self):
        root = {}
        root['__class'] = self.__class__.__name__
        root['id'] = self.id
        root['email'] = self.email
        root['goals'] = self.user_goals
        # root['interests'] = self.user_goals['interests']
        return root

    def user_groups_for_json(self):
        root = {}
        root['__class'] = self.__class__.__name__
        root['id'] = self.id
        root['email'] = self.email
        root['groups'] = self.user_groups
        return root


    def user_locations_for_json(self, auth_id):
        root = {}
        root['__class'] = self.__class__.__name__
        root['id'] = self.id
        if self.id == auth_id:
            root ['allow_edit'] = True
        return root

    def local_users_with_shared_interests_for_json(self):
        root = {}
        root['__class'] = self.__class__.__name__
        root['id'] = self.id
        root['email'] = self.email
        root['users'] = self.get_local_users_shared_interests_near_location()
        return root

    def activated_user_for_json(self):
        root = {}
        root['__class'] = self.__class__.__name__
        root['x_auth_key'] = self.permanent_web_token
        return root

