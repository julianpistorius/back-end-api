__author__ = 'marnee'
from jsonschema import validate

goal_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "id": "/",
  "type": "object",
  "properties": {
    "goal": {
      "id": "goal",
      "type": "object",
      "properties": {
        "title": {
          "id": "title",
          "type": "string"
        },
        "description": {
          "id": "description",
          "type": "string"
        },
        "start_date": {
          "id": "start_date",
          "type": "string"
        },
        "end_date": {
          "id": "end_date",
          "type": "string"
        },
        "is_public": {
          "id": "is_public",
          "type": "boolean"
        },
        "achieved": {
          "id": "achieved",
          "type": "boolean"
        }
      },
      "required": [
        "title",
        "description",
        "start_date",
        "end_date",
        "is_public",
        "achieved"
      ]
    }
  },
  "required": [
    "goal"
  ]
}

#TODO return object with why json validation failed


def validate_goal(goal_json):
    try:
        validate(goal_json, goal_schema)
        return True
    except:
        return False

