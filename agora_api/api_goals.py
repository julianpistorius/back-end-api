__author__ = 'Marnee Dearman'
from agora_db.goal import AgoraGoal
import simplejson
from api_serializers import GoalResponder
import falcon
import simplejson


def get_goal(id):
    agora_goal = AgoraGoal()
    agora_goal.id = id
    agora_goal.get_goal()
    return agora_goal


class Goal(object):
    def __init__(self):
        pass

    def on_get(self, request, response, goal_id):
        response.data = self.get_goal_json(goal_id)
        response.content_type = 'application/json'
        response.status = falcon.HTTP_200

    def on_post(self, request, response):
        pass
    #TODO add logic to create and update goals

    def on_put(self, request, response):
        pass
    #TODO add logic to update goal


    def get_goal_json(self, goal_id):
        goal = get_goal(goal_id).goal_for_json()
        json = GoalResponder.respond(goal, links={'interests': goal['interests']})
        return json

    def create_goal(self, goal_json):
        pass

