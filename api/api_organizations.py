__author__ = 'Marnee Dearman'
import falcon
from db.organization import Organization
from db.auth import Auth
import simplejson
from api_serializers import OrganizationResponder
from validators import validate_organization_schema


def user_auth(request):
    auth = Auth(auth_header=request.headers)
    return auth


class ApiOrganization(object):
    def __init__(self):
        pass

    def on_get(self, request, response, org_id=None):
        """
        get organization
        :param request:
        :param response:
        :param org_id:
        :return:
        """
        #TODO get list of orgs
        response.data = self.get_org(org_id)
        response.content_type = 'application/json'
        response.status = falcon.HTTP_200

    def on_post(self, request, response):
        """
        create organization
        :param request:
        :param response:
        :param org_id:
        :return:
        """
        #TODO check authorizes user
        raw_json = request.stream.read()
        result_json = simplejson.loads(raw_json, encoding='utf-8')
        if validate_organization_schema.validate_organization(result_json):
            self.create_org(result_json['organization'])
            response.status = falcon.HTTP_201
        else:
            response.status = falcon.HTTP_400

    def on_put(self, request, response, org_id):
        """
        update organization
        :param request:
        :param response:
        :param org_id:
        :return:
        """
        raw_json = request.stream.read()
        result_json = simplejson.loads(raw_json, encoding='utf-8')
        #TODO check authorized user
        if validate_organization_schema.validate_organization(result_json):
            self.update_org(result_json['organization'])
            response.status = falcon.HTTP_201
        else:
            response.status = falcon.HTTP_400

    def get_org(self, org_id):
        org = Organization()
        org.id = org_id
        org.get_organization()
        org_details = org.organization_relationships_for_json()
        json = OrganizationResponder.respond(org_details, linked={'interests': org_details['interests'],
                                                                  'members': org_details['members']})
        return json

    def create_org(self, org_json):
        org = Organization()
        org.set_organization_attributes(org_json)
        #TODO create org
        #TODO link org to creator

    def update_org(self, org_json):
        org = Organization()
        org.set_organization_attributes(org_json)
        #TODO update org
        #CHECK can edit org (see group)


class ApiOrganizationUsers(object):
    def __init__(self):
        pass

    def on_get(self, request, response, org_id):
        #TODO get organiztion's users
        pass

    def get_org_users_json(self, org_id):
        pass


class ApiOrganizationInterests(object):
    def __init__(self):
        pass

    def on_get(self, request, response, org_id):
        #TODO get org's interests
        pass

    def get_org_interests_json(self, org_id):
        pass