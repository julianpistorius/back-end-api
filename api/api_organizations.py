__author__ = 'Marnee Dearman'
import falcon
from db.organization import Organization
from api_serializers import OrganizationResponder
from validators.validate_organization_schema import validate_organization
from validators.validate_location_schema import validate_location
from base import ApiBase


class ApiOrganization(ApiBase):
    def on_get(self, request, response, org_id=None):
        """
        get organization
        :param request:
        :param response:
        :param org_id:
        :return:
        """
        #TODO get list of orgs
        # response.data = self.get_org(org_id)
        # response.content_type = 'application/json'
        # response.status = falcon.HTTP_200

    def on_post(self, request, response):
        """
        create organization
        :param request:
        :param response:
        :param org_id:
        :return:
        """
        if self.validate_json(request, validate_organization):
            self.create_org(self.result_json['organization'])
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
        # #TODO check authorized user
        if self.validate_json(request, validate_organization):
            self.update_org(self.result_json['organization'])
            response.status = falcon.HTTP_201
        else:
            response.status = falcon.HTTP_400

    def get_org_responder(self, org_id):
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
        # CHECK can edit org (see group)


class ApiOrganizationLocations(ApiBase):
    # GET list of locations for the organization
    def on_get(self, request, response, org_id):
        response.content_type = 'application/json'
        response.status = falcon.HTTP_200
        response.data = self.get_organization_responder(org_id)

    # POST add/create a location for an organization
    def on_post(self, request, response, org_id):
        if self.authorize_user(request):
            if self.validate_json(request, validate_location):
                org = self.get_organization(org_id)
                org.add_location(self.result_json['location'])
                response.data = self.get_organization_responder(org_id)
                response.content_type = 'application/json'
                response.status = falcon.HTTP_201
            else:
                response.status = falcon.HTTP_401  # unauthorized
        else:
            response.status = falcon.HTTP_400  # bad request

    # DELETE drop location  #TODO
    def on_delete(self, request, response, org_id, location_id):
        pass

    def get_organization_responder(self, org_id):
        org = self.get_organization(org_id)
        org_data = org.organization_relationships_for_json()
        return OrganizationResponder.respond(org_data,
                                             linked={'locations': org_data['locations']})


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