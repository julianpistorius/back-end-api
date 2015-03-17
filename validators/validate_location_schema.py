__author__ = 'marnee'
from jsonschema import validate

location_schema = {
  "$schema": "http://json-schema.org/draft-04/schema#",
  "id": "/",
  "type": "object",
  "properties": {
    "location": {
      "id": "location",
      "type": "object",
      "properties": {
        "formatted_address": {
          "id": "formatted_address",
          "type": "string"
        },
        "name": {
          "id": "name",
          "type": "string"
        },
        "id": {
          "id": "id",
          "type": "string"
        }
      },
      "required": [
        "formatted_address",
        "name",
        "id"
      ]
    }
  },
  "required": [
    "location"
  ]
}

#TODO return object with why json validation failed


def validate_location(location_json):
    try:
        validate(location_json, location_schema)
        return True
    except:
        return False
