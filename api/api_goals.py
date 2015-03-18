__author__ = 'Marnee Dearman'
from db.goal import Goal
import simplejson
from api_serializers import GoalResponder
import falcon
import simplejson
from db.auth import Auth
from validators import validate_goals_schema


def get_goal(id):
    agora_goal = Goal()
    agora_goal.id = id
    agora_goal.get_goal()
    return agora_goal


def user_auth(request):
    auth = Auth(auth_header=request.headers)
    return auth


class ApiGoal(object):
    def __init__(self):
        pass

    def on_get(self, request, response, goal_id):
        auth = user_auth(request)
        response.data = self.get_goal_json(goal_id, auth.auth_key)
        response.content_type = 'application/json'
        response.status = falcon.HTTP_200

    def on_post(self, request, response):
        raw_json = request.stream.read()
        result_json = simplejson.loads(raw_json, encoding='utf-8')
        if validate_goals_schema.validate_goal(result_json):
            pass
        else:
            response.status = falcon.HTTP_400

    def on_put(self, request, response, goal_id):
        raw_json = request.stream.read()
        result_json = simplejson.loads(raw_json, encoding='utf-8')
        if validate_goals_schema.validate_goal(result_json):
            pass
        else:
            response.status = falcon.HTTP_400

    def get_goal_json(self, goal_id, auth_id):
        #TODO return only the data the user can see and the allow edits
        goal = get_goal(goal_id).goal_for_json()
        json = GoalResponder.respond(goal, links={'interests': goal['interests']})
        return json

    #TODO add logic to create goal
    def create_goal(self, goal_json):
        pass

    #TODO add logic to update goal
    def update_goal(self, goal_json):
        pass
