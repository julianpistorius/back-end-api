__author__ = 'marnee'
from jsonschema import validate

meeting_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "id": "/",
  "type": "object",
  "properties": {
    "meeting": {
      "id": "meeting",
      "type": "object",
      "properties": {
        "name": {
          "id": "name",
          "type": "string"
        },
        "description": {
          "id": "description",
          "type": "string"
        },
        "where": {
          "id": "where",
          "type": "string"
        },
        "date": {
          "id": "date",
          "type": "string"
        },
        "time": {
          "id": "time",
          "type": "string"
        }
      },
      "required": [
        "name",
        "description",
        "where",
        "date",
        "time"
      ]
    }
  },
  "required": [
    "meeting"
  ]
}

#TODO return object with why json validation failed


def validate_meeting(meeting_json):
    try:
        validate(meeting_json, meeting_schema)
        return True
    except:
        return False


