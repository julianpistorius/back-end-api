__author__ = 'marnee'
from jsonschema import validate

cq_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "id": "/",
  "type": "object",
  "properties": {
    "cq": {
      "id": "cq",
      "type": "object",
      "properties": {
        "subject": {
          "id": "subject",
          "type": "string"
        },
        "message": {
          "id": "message",
          "type": "string"
        },
        "interests": {
          "id": "interests",
          "type": "array",
          "items": [
            {
              "id": "0",
              "type": "string"
            },
            {
              "id": "1",
              "type": "string"
            }
          ]
        }
      },
      "required": [
        "subject",
        "message"
      ]
    }
  },
  "required": [
    "cq"
  ]
}


def validate_cq(cq_json):
    try:
        validate(cq_json, cq_schema)
        return True
    except:
        return False