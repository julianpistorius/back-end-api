__author__ = 'Marnee Dearman'
from jsonschema import validate

user = {"user": {"permanent_web_token": "ImE4OGFjYTAwLTU5YmMtNDVkZC1iYWI3LTk4OTkyMGJjMTVhZCI.gahZ0HSB_D9SYPPA2g-pFz5zfqI", "id": "a88aca00-59bc-45dd-bab7-989920bc15ad"}}

schema = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "id": "",
    "type": "object",
    "properties": {
        "user": {
            "id": "/user",
            "type": "object",
            "properties": {
                "permanent_web_token": {
                    "id": "/user/permanent_web_token",
                    "type": "string"
                },
                "id": {
                    "id": "/user/id",
                    "type": "string"
                }
            },
            "required": [
                "permanent_web_token",
                "id"
            ]
        }
    },
    "required": [
        "user"
    ]
}
validate(user, schema)