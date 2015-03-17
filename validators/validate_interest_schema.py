__author__ = 'marnee'
from jsonschema import validate

interest_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "id": "/",
  "type": "object",
  "properties": {
    "interest": {
      "id": "interest",
      "type": "object",
      "properties": {
        "id": {
          "id": "id",
          "type": "string"
        },
        "experience": {
          "id": "experience",
          "type": "string"
        },
        "time": {
          "id": "time",
          "type": "string"
        }
      },
      "required": [
        "id",
        "experience",
        "time"
      ]
    }
  },
  "required": [
    "interest"
  ]
}
#TODO return object with why json validation failed


def validate_interest(interest_json):
    try:
        validate(interest_json, interest_schema)
        return True
    except:
        return False


