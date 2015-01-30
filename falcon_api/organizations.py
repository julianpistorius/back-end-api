__author__ = 'Marnee Dearman'
import falcon
from agora_db.py2neo_organization import AgoraOrganization
from agora_db.py2neo_user import AgoraUser
from agora_db.py2neo_interest import AgoraInterest
import simplejson
from serializers import OrganizationResponder

class Organization(object):
    def __init__(self):
        pass

    #TODO check tokens on api calls
    def check_token(self):
        pass

    def on_get(self, request, response, org_id=None):
        """
        get organization
        :param request:
        :param response:
        :param org_id:
        :return:
        """
        response.data = self.get_org(org_id)
        response.content_type = 'application/json'
        response.status = falcon.HTTP_200

    def on_post(self, request, response, org_id=None):
        """
        create organization
        :param request:
        :param response:
        :param org_id:
        :return:
        """
        raw_json = request.stream.read()
        result_json = simplejson.loads(raw_json, encoding='utf-8')
        self.create_org(result_json['organization'])
        response.status = falcon.HTTP_202

    def on_put(self, request, response, org_id=None):
        """
        update organization
        :param request:
        :param response:
        :param org_id:
        :return:
        """
        raw_json = request.stream.read()
        result_json = simplejson.loads(raw_json, encoding='utf-8')
        self.update_org(result_json['organization'])
        response.status = falcon.HTTP_202

    def get_org(self, org_id):
        org = AgoraOrganization()
        org.id = org_id
        org.get_organization()
        org_details = org.organization_relationships_for_json()
        json = OrganizationResponder.respond(org_details, linked={'interests': org_details['interests'],
                                                                  'members': org_details['members']})
        return json

    def create_org(self, org_json):
        org = AgoraOrganization()
        org.set_org_attributes(org_json)


    def update_org(self, org_json):
        org = AgoraOrganization()
        org.set_org_attributes(org_json)
        #TODO update org


class OrganizationUsers(object):
    def __init__(self):
        pass

    def on_get(self, request, response, org_id):
        #TODO get organiztion's users
        pass

    def get_org_users_json(self, org_id):
        pass


class OrganizationInterests(object):
    def __init__(self):
        pass

    def on_get(self, request, response, org_id):
        #TODO get org's interests
        pass

    def get_org_interests_json(self, org_id):
        pass