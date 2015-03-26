__author__ = 'marnee'
import functools
from validators import validate_user_schema


def validate_json(object_type):
    def _check_type(func):
        def _validate(json_obj, *args, **kwargs):
            # validate json
            if object_type == "activate":
                if validate_user_schema.validate_activate_user(json_obj):
                    return func(json_obj)
                else:
                    return False
        return functools.wraps(func)(_validate)
    return _check_type
