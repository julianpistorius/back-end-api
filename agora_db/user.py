_author__ = 'Marnee Dearman'
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
# from simplecrypt import encrypt, decrypt
# from py2neo import neo4j
from agora_types import AgoraRelationship, AgoraLabel
# import time
from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer, BadSignature, BadTimeSignature
from agora_services import smtp


class AgoraUser(object):
    def __init__(self, graph_db=None):
        self.name = ''
        self.id = ''
        self.mission_statement = ''
        self.about = ''
        self.email = ''
        self.is_mentor = False
        self.is_tutor = False
        self.is_visible = True
        self.is_available_for_in_person = True
        # self._interests_list = None
        self.is_admin = False
        self.password = ''
        self.salt = ''
        self.permanent_web_token = ''
        self.temporary_web_token = ''
        self.join_date = None
        self.graph_db = Graph(settings.DATABASE_URL)

    @property
    def user_properties(self):
        """
        setup user properties
        :return: dictionary of properties
        """
        properties_dict = dict(self.__dict__)
        del properties_dict['graph_db']
        return properties_dict

    def set_user_properties(self, user_properties):
        for key, value in user_properties.iteritems():
            setattr(self, key, value)

    def get_user(self):
        user_node = self.user_node
        if user_node is not None:
            user_properties = dict(user_node.properties)
            for key, value in user_properties.iteritems():
                setattr(self, key, value)

    def create_user(self, user_properties=None):
        """
        create a new user based on the attributes
        :return: node
        """
        #TODO exception handling
        self.join_date = datetime.date.today()
        self.id = str(uuid.uuid4())
        if not user_properties is None:
            self.set_user_properties(user_properties)
        # new_user_node = Node.cast(AgoraLabel.USER, self.user_properties)

        new_user_node = Node.cast(AgoraLabel.USER, self.user_properties)
        try:
            self.graph_db.create(new_user_node)
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
        return self.graph_db.find_one(AgoraLabel.USER,
                                      property_key='email',
                                      property_value=self.email)
        # return self.graph_db.get_or_create_indexed_node(index_name=AgoraLabel.USER,
        #                                                      key='email', value=self.email)

    @property
    def user_interests(self):
        """ get user interests
        :return: dictionary of interests
        """
        user_interests = self.graph_db.match(start_node=self.user_node,
                                             rel_type=AgoraRelationship.INTERESTED_IN,
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
        #TODO add list of interests
        user_goals = self.graph_db.match(start_node=self.user_node, rel_type=AgoraRelationship.HAS_GOAL,
                                         end_node=None)
        #create a list of tuples of interests and the users's relationship to them
        goals_list = []
        goal_interests_list = []
        for rel in user_goals:
            goal_properties = dict(rel.end_node.properties)
            goal = AgoraGoal()
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
        user_groups = self.graph_db.match(start_node=self.user_node, rel_type=AgoraRelationship.STUDIES_WITH,
                                          end_node=None)
        #create a list of tuples of interests and the users's relationship to them
        groups_list = []
        for rel in user_groups:
            group_properties = dict(rel.end_node.properties)
            group = AgoraGroup()
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
        user_orgs = self.graph_db.match(start_node=self.user_node,
                                        rel_type=AgoraRelationship.MEMBER_OF,
                                        end_node=None)
        orgs_list = []
        for rel in user_orgs:
            org_properties = dict(rel.end_node.properties)
            org = AgoraOrganization()
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
        user_locations = self.graph_db.match(start_node=self.user_node,
                                        rel_type=AgoraRelationship.LOCATED_IN,
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
            'email': 'marnee@agorasociety.com'
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
        interest = AgoraInterest()
        interest.id = interest_id
        # interest.get_interest_by_id()
        interest_node = interest.interest_node_by_id
        # user_interest_relationship = Relationship(start_node=self.user_node,
        #                                           rel=AgoraRelationship.INTERESTED_IN,
        #                                           end_node=interest_node)
        user_interest_relationship = Relationship(self.user_node,
                                                  AgoraRelationship.INTERESTED_IN,
                                                  interest_node)
                                                  # properties=experience_properties_dict)
        # user_interest_relationship.properties = experience_properties_dict
        for key, value in experience_properties_dict.iteritems():
            user_interest_relationship[key] = value
        try:
            self.graph_db.create_unique(user_interest_relationship)
        except:
            pass
        return self.user_interests

    def update_interest(self, interest_id, experience_properties_dict):
        interest = AgoraInterest()
        interest.id = interest_id
        # interest.get_interest_by_id()
        interest_node = interest.interest_node_by_id
        #TODO find out why binding does not work ask on Stack Overflow
        user_interest_relationship = self.graph_db.match_one(start_node=self.user_node,
                                                             rel_type=AgoraRelationship.INTERESTED_IN,
                                                             end_node=interest_node)
        # user_interest_relationship = Relationship(start_node=self.user_node,
        #                                           rel=AgoraRelationship.INTERESTED_IN,
        #                                           end_node=interest_node)
        #                                           # properties=experience_properties_dict)
        # user_interest_relationship.properties = experience_properties_dict
        for key, value in experience_properties_dict.iteritems():
            user_interest_relationship.properties[key] = value
        user_interest_relationship.push()

        # user_interest_relationship.bind(uri=Graph().uri)
        # self.graph_db.push(user_interest_relationship)
        # user_interest_relationship.bind(uri=self.graph_db.uri, metadata=None)
        # user_interest_relationship.push()

    def update_user(self):
        user_node = self.user_node
        user_properties = dict(self.user_properties)
        for key, value in user_properties.iteritems():
            user_node[key] = value #user_properties[key]
        # self.user_node.properties = self.user_properties
        # print self.graph_db.uri
        # user_node.bind(self.graph_db.uri)
        user_node.push()

    # def make_admin(self):
    #     #new_user = self.graph_db.get_or_create_indexed_node(index_name=AgoraLabel.USER, key='email', value=self.email)
    #     self.user_node.add_labels(AgoraLabel.ADMIN)

    def add_goal(self, goal_id, goal_relationship_properties=None):
        """
        Add goal to user
        :param goal_id: string uuid
        :return: List of user goals
        """
        #TODO exception handling
        goal = AgoraGoal()
        goal.id = goal_id
        #create relationship between user and interest node
        user_goal_relationship = Relationship(self.user_node,
                                              AgoraRelationship.HAS_GOAL,
                                              goal.goal_node)

        self.graph_db.create_unique(user_goal_relationship)
        #TODO set properties on the relationship -- may use a unique id as the key
        return self.user_goals

    def delete_goal(self, goal_id):
        user_node = self.user_node
        goal = AgoraGoal()
        goal.id = goal_id
        #have to remove all relationships before deleteing a node
        goal.delete_all_interests()
        goal_node = goal.goal_node
        user_goal_rel = self.graph_db.match_one(start_node=user_node,
                                                rel_type=AgoraRelationship.HAS_GOAL,
                                                end_node=goal_node)
        self.graph_db.delete(user_goal_rel)
        self.graph_db.delete(goal_node)

    def join_group(self, group_id, group_relationship_properties=None):
        """
        Add user as member of group
        :param group_id: string uuid
        :return:
        """
        #TODO exception handling
        group = AgoraGroup()
        group.id = group_id
        #relationship properties
        join_properties = {
            'join_date': datetime.date.today()
        }
        user_group_relationship = Relationship(self.user_node,
                                               AgoraRelationship.STUDIES_WITH,
                                               group.group_node)
                                               # properties=join_properties)
        for key, value in join_properties.iteritems():
            user_group_relationship[key] = value
        try:
            self.graph_db.create_unique(user_group_relationship)
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
        group = AgoraGroup()
        group.id = group_id
        user_group_relationship = self.graph_db.match_one(start_node=self.user_node,
                                                          rel_type=AgoraRelationship.MEMBER_OF,
                                                          end_node=group.group_node)

        self.graph_db.delete(user_group_relationship)

    def delete_group(self, group_id):
        pass

    def join_organization(self, organization_id):
        """
        add user to organization
        :param organization_id: string uuid
        :return: list of tuple of interests
        """
        #TODO exception handling
        org = AgoraOrganization()
        org.id = organization_id

        user_org_relationship = Relationship(self.user_node,
                                             AgoraRelationship.MEMBER_OF,
                                             org.org_node)
        try:
            self.graph_db.create_unique(user_org_relationship)
        except:
            print sys.exc_info()[0]

    def leave_organization(self, organization_id):
        """
        remove relationship between user and organization
        :param organization_id:
        :return:
        """
        #TODO exception handling
        org = AgoraOrganization()
        org.id = organization_id
        user_org_relationship = self.graph_db.match_one(start_node=self.user_node,
                                                        rel_type=AgoraRelationship.MEMBER_OF,
                                                        end_node=org.org_node)
        self.graph_db.delete(user_org_relationship)

    def add_location(self, location_place_id):
        """
        link user to location nodes
        :param locations_place_id:
        :return:
        """
        #TODO exception handling
        location = AgoraLocation()
        location.place_id = location_place_id

        user_location_relationship = Relationship(self.user_node,
                                                  AgoraRelationship.LOCATED_IN,
                                                  location.location_node_by_place_id)
        # try:
        self.graph_db.create_unique(user_location_relationship)
        # except:
        #     pass

    def register_user(self, email):
        verification_email = smtp.AgoraSmtp()
        verification_email.recipients = [email]
        s = URLSafeTimedSerializer(secret_key=settings.TOKEN_SECRET_KEY)
        payload = s.dumps(email)
        verification_email.subject = settings.ACTIVATION_SUBJECT
        verification_email.message = settings.ACTIVATION_MESSAGE
        verification_email.url = self.construct_verification_url(payload=payload)
        verification_email.send_by_gmail()

    def activate_user(self, payload, email):
        s = URLSafeTimedSerializer(secret_key=settings.TOKEN_SECRET_KEY)
        payload_email = s.loads(payload, max_age=settings.TOKEN_EXPIRES_IN)  # 10 minutes
        if email == payload_email:
            self.email = email
            self.get_user()
            self.permanent_web_token = self.create_web_token()
            if self.id == '':
                self.create_user()
            else:
                self.update_user()
        else:
            raise BadSignature('bad email')


    def construct_verification_url(self, payload):
        return settings.SITE_URL + "/" + settings.ACTIVATION_ROUTE + "/%s" % payload

    def create_web_token(self):
        s = URLSafeSerializer(secret_key=settings.TOKEN_SECRET_KEY)
        return s.dumps(self.id)

    def user_relationships_for_json(self):
        root = self.user_profile_for_json()
        root['interests'] = self.user_interests
        root['locations'] = self.user_locations
        root['goals'] = self.user_goals
        root['groups'] = self.user_groups
        root['organizations'] = self.user_orgs
        return root

    def user_profile_for_json(self):
        root = self.user_properties
        return root


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


    def user_locations_for_json(self):
        root = {}
        root['__class'] = self.__class__.__name__
        root['id'] = self.id
        root['email'] = self.email
        root['locations'] = self.user_locations
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
        root['id'] = self.id
        root['permanent_web_token'] = self.permanent_web_token
        return root

