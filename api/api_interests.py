__author__ = 'Marnee Dearman'
import falcon
from db.auth import Auth
from db.user import User
from db.interest import Interest
from base import ApiBase
from validators.validate_interest_schema import validate_interest
import simplejson
from api_serializers import InterestResponder, SearchResponder


class ApiInterest(ApiBase):

    def on_get(self, request, response, interest_id=None):
        """

        :param request:
        :param response:
        :param interest_id:
        :return:
        """
        if interest_id is not None:
            response.data = self.get_interest(interest_id)
        else:
            match = request.params['match']
            limit = int(request.params['limit'])
            search_results = Interest().matched_interests(match_string=match,
                                                               limit=limit)
            response.data = SearchResponder.respond(search_results,
                                                    linked={'interests': search_results['interests']})
        response.content_type = 'application/json'
        response.status = falcon.HTTP_200

    def on_post(self, request, response, interest_id):
        """
        create interest
        :param request:
        :param response:
        :param interest_id:
        :return:
        """
        if self.validate_json(request, validate_interest):
            self.create_interest(self.result_json['interest'])
            response.status = falcon.HTTP_201
        else:
            response.status = falcon.HTTP_400

    def create_interest(self, interest_json):
        interest = Interest()
        interest.set_interest_attributes(interest_json)
        interest.create_interest()

    def get_interest(self, interest_id):
        interest = Interest()
        interest.id = interest_id
        interest.get_interest_by_id()
        interest_details = interest.get_interest_for_json()
        json = InterestResponder.respond(interest_details)
        return json
