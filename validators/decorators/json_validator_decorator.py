
__author__ = 'marnee'
import functools
import simplejson
from validators.validate_user_schema import validate_user, validate_activate_user


def validate_json(object_type):
    def _check_type(func):
        def _validate(json_obj, *args, **kwargs):
            # validate json
            if object_type == "activate":
                if validate_activate_user(json_obj):
                    return func(json_obj)
                else:
                    return False
        return functools.wraps(func)(_validate)
    return _check_type


def validate_request_json(object_type):
    def _check_type(func):

        def _validate(self, request, response):
            raw_json = request.stream.read()
            result_json = simplejson.loads(raw_json, encoding='utf-8')
            if object_type == "register":
                if validate_activate_user(result_json):
                    return func(self, request, response)
                else:
                    return False
        return functools.wraps(func)(_validate)
    return _check_type
