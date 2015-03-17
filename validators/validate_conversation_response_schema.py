__author__ = 'marnee'
from jsonschema import validate

conversation_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "id": "/",
  "type": "object",
  "properties": {
    "conversation": {
      "id": "conversation",
      "type": "object",
      "properties": {
        "subject": {
          "id": "subject",
          "type": "string"
        },
        "message": {
          "id": "message",
          "type": "string"
        }
      },
      "required": [
        "subject",
        "message"
      ]
    }
  },
  "required": [
    "conversation"
  ]
}


#TODO return object with why json validation failed


def validate_conversation(conversation_json):
    try:
        validate(conversation_json, conversation_schema)
        return True
    except:
        return False

