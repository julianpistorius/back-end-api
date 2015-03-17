__author__ = 'marnee'
from jsonschema import validate

organization_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "id": "/",
  "type": "object",
  "properties": {
    "organization": {
      "id": "organization",
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
    "organization"
  ]
}

#TODO return object with why json validation failed


def validate_organization(organization_json):
    try:
        validate(organization_json, organization_schema)
        return True
    except:
        return False


