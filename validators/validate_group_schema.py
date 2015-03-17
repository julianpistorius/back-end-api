__author__ = 'marnee'
from jsonschema import validate

group_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "id": "/",
  "type": "object",
  "properties": {
    "group": {
      "id": "group",
      "type": "object",
      "properties": {
        "name": {
          "id": "name",
          "type": "string"
        },
        "about": {
          "id": "about",
          "type": "string"
        },
        "mission_statement": {
          "id": "mission_statement",
          "type": "string"
        },
        "is_open": {
          "id": "is_open",
          "type": "boolean"
        },
        "is_invite_only": {
          "id": "is_invite_only",
          "type": "boolean"
        },
        "website": {
          "id": "website",
          "type": "string"
        }
      },
      "required": [
        "name",
        "about",
        "mission_statement",
        "is_open",
        "is_invite_only"
      ]
    }
  },
  "required": [
    "group"
  ]
}

#TODO return object with why json validation failed


def validate_group(group_json):
    try:
        validate(group_json, group_schema)
        return True
    except:
        return False


