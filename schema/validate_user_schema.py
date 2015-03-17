__author__ = 'marnee'
from jsonschema import validate

activate_user_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "id": "/",
  "type": "object",
  "properties": {
    "user": {
      "id": "user",
      "type": "object",
      "properties": {
        "email": {
          "id": "email",
          "type": "string"
        }
      },
      "required": [
        "email"
      ]
    }
  },
  "required": [
    "user"
  ]
}

user_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "id": "/",
  "type": "object",
  "properties": {
    "user": {
      "id": "user",
      "type": "object",
      "properties": {
        "name": {
          "id": "name",
          "type": "string"
        },
        "call_sign": {
          "id": "call_sign",
          "type": "string"
        },
        "first_name": {
          "id": "first_name",
          "type": "string"
        },
        "last_name": {
          "id": "last_name",
          "type": "string"
        },
        "mission_statement": {
          "id": "mission_statement",
          "type": "string"
        },
        "about": {
          "id": "about",
          "type": "string"
        },
        "email": {
          "id": "email",
          "type": "string"
        },
        "is_mentor": {
          "id": "is_mentor",
          "type": "boolean"
        },
        "is_visible": {
          "id": "is_visible",
          "type": "boolean"
        },
        "is_available_for_in_person": {
          "id": "is_available_for_in_person",
          "type": "boolean"
        }
      },
      "required": [
        "name",
        "call_sign",
        "first_name",
        "last_name",
        "mission_statement",
        "about",
        "email",
        "is_mentor",
        "is_visible",
        "is_available_for_in_person"
      ]
    }
  },
  "required": [
    "user"
  ]
}

#TODO return object with why json validation failed

def validate_activate_user(self, activate_user):
    try:
        validate(activate_user, activate_user_schema)
        return True
    except:
        return False


def validate_user(self, user):
    try:
        validate(user, user_schema)
        return True
    except:
        return False
