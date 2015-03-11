__author__ = 'Marnee Dearman'
from marshmallow import Schema, fields
from hyp.marshmallow import Responder
import settings


class UserSchema(Schema):
    id = fields.String()
    name = fields.String()
    call_sign = fields.String()
    mission_statement = fields.String()
    about = fields.String()
    last_active_date = fields.Date()
    join_date = fields.Date()
    is_mentor = fields.Boolean()
    is_tutor = fields.Boolean()
    is_visible = fields.Boolean()
    is_available = fields.Boolean()
    is_admin = fields.Boolean()
    is_owner = fields.Boolean()
    allow_edit = fields.Boolean()
    allow_message = fields.Boolean()


class InterestSchema(Schema):
    # interests = fields.List(fields)
    name = fields.String()
    id = fields.String()
    description = fields.String()
    experience = fields.String()
    time = fields.String()


class GoalSchema(Schema):
    id = fields.String()
    title = fields.String()
    description = fields.String()
    start_date = fields.String()
    end_date = fields.String()
    created_date = fields.String()
    is_public = fields.String()


class GroupSchema(Schema):
    id = fields.String()
    name = fields.String()
    about = fields.String()
    is_open = fields.Boolean()
    is_invite_only = fields.Boolean()
    website = fields.String()


class OrganizationSchema(Schema):
    id = fields.String()
    name = fields.String()
    mission_statement = fields.String()
    about = fields.String()
    email = fields.String()
    is_open = fields.String()
    is_invite_only = fields.String()
    is_visible = fields.Boolean()
    website = fields.String()


class LocationSchema(Schema):
    id = fields.String()
    name = fields.String()
    formatted_address = fields.String()


class ActivatedUserSchema(Schema):
    x_auth_key = fields.String()


class ResultsSchema(Schema):
    count = fields.Integer()


class UserResponder(Responder):
    TYPE = 'users'
    SERIALIZER = UserSchema


class SearchResponder(Responder):
    TYPE = 'results'
    SERIALIZER = ResultsSchema


class ActivatedUserResponder(Responder):
    TYPE = 'activationkey'
    SERIALIZER = ActivatedUserSchema


class InterestResponder(Responder):
    TYPE = 'interests'
    SERIALIZER = InterestSchema


class GoalResponder(Responder):
    TYPE = 'goals'
    SERIALIZER = GoalSchema


class GroupResponder(Responder):
    TYPE = 'groups'
    SERIALIZER = GroupSchema


class LocationResponder(Responder):
    TYPE = 'locations'
    SERIALIZER = LocationSchema


class OrganizationResponder(Responder):
    TYPE = 'organizations'
    SERIALIZER = OrganizationSchema


SearchResponder.LINKS = {
    'users': {
        'responder': UserResponder,
        'href': '%s/users/{users.id}' % (settings.SITE_URL)
    },
    'interests': {
        'responder': InterestResponder,
        'href': '%s/interests/{interests.id}' % (settings.SITE_URL)
    },
    'groups': {
        'responder': GroupResponder,
        'href': '%s/groups/{groups.id}' % (settings.SITE_URL)
    }
}

ActivatedUserResponder.LINKS = {
    'users': {
        'responder': UserResponder,
        'href': '%s/users/{users.id}' % (settings.SITE_URL)
    }
}

InterestResponder.LINKS = {
    'users': {
        'responder': UserResponder,
        'href': '%s/users/{users.id}' % (settings.SITE_URL)
    },
    'groups': {
        'responder': GroupResponder,
        'href': '%s/groups/{groups.id}' % (settings.SITE_URL)
    }
}

GoalResponder.LINKS = {
    'interests': {
        'responder': InterestResponder,
        'href': '%s/interests/{interests.id}' % (settings.SITE_URL)
    }
}

GroupResponder.LINKS = {
    'interests': {
        'responder': InterestResponder,
        'href': '%s/groups/{groups.id}/interests/{interests.id}' % (settings.SITE_URL)
    },
    'goals': {
        'responder': GoalResponder,
        'href': '%s/groups/{groups.id}/goals/{goals.id}' % (settings.SITE_URL)
    },
    'users': {
        'responder': UserResponder,
        'href': '%s/users/{users.id}' % (settings.SITE_URL)
    }
}

LocationResponder.LINKS = {
    'interests': {
        'responder': InterestResponder,
        'href': '%s/groups/{groups.id}/interests/{interests.id}' % (settings.SITE_URL)
    },
    'users': {
        'responder': UserResponder,
        'href': '%s/users/{users.id}' % (settings.SITE_URL)
    },
    'groups': {
        'responder': GroupResponder,
        'href': '%s/groups/{groups.id}' % (settings.SITE_URL)
    }
}

OrganizationResponder.LINKS = {
    'interests': {
        'responder': InterestResponder,
        'href': '%s/groups/{groups.id}/interests/{interests.id}' % (settings.SITE_URL)
    },
    'goals': {
        'responder': GoalResponder,
        'href': '%s/groups/{groups.id}/goals/{goals.id}' % (settings.SITE_URL)
    },
    'users': {
        'responder': UserResponder,
        'href': '%s/users/{users.id}' % (settings.SITE_URL)
    },
    'groups': {
        'responder': GroupResponder,
        'href': '%s/groups/{groups.id}' % (settings.SITE_URL)
    }
}

UserResponder.LINKS = {
    'interests': {
        'responder': InterestResponder,
        'href': '%s/users/{users.id}/interests/{interests.id}' % (settings.SITE_URL)
    },
    'groups': {
        'responder': GroupResponder,
        'href': '%s/groups/{group.id}' % (settings.SITE_URL)
    },
    'locations': {
        'responder': LocationResponder,
        'href': '%s/locations/{locations.id}' % (settings.SITE_URL)
    },
    'goals': {
        'responder': GoalResponder,
        'href': '%s/users/{users.id}/goals/{goal.id}' % (settings.SITE_URL)
    },
    'organizations': {
        'responder': OrganizationResponder,
        'href': '%s/organizations/{organization.id}' % (settings.SITE_URL)
    }
}


# class UserInterestsResponder(Responder):
# TYPE = 'users'
# SERIALIZER = UserSchema
# LINKS = {
# 'interests': {
#             'responder': InterestResponder,
#             'href': '%s/interests/{interests.id}' % (settings.SITE_URL)
#         }
#     }


# class GoalInterestResponder(Responder):
#     TYPE = 'goals'
#     SERIALIZER = GoalSchema
#     LINKS = {
#         'interests': {
#             'responder': InterestResponder,
#             'href': '%s/goals/{goals.id}/interests/{interests.id}' % (settings.SITE_URL)
#         }
#     }


# class UserGoalsResponder(Responder):
#     TYPE = 'user'
#     SERIALIZER = UserSchema
#     LINKS = {
#         'goals': {
#             'responder': GoalResponder,
#             'href': '%s/users/{user.id}/goals/{goal.id}' % (settings.SITE_URL)
#         }
#     }


# class UserLocationsResponder(Responder):
#     TYPE = 'user'
#     SERIALIZER = UserSchema
#     LINKS = {
#         'locations': {
#             'responder': LocationResponder,
#             'href': '%s/locations/{locations.id}'
#         }
#     }




# class UserGroupsResponder(Responder):
#     TYPE = 'user'
#     SERIALIZER = UserGroupsSchema
#     LINKS = {
#         'groups': {
#             'responder': GroupResponder
#         },
#     }



# class UserOrganizationsResponder(Responder):
#     TYPE = 'users'
#     SERIALIZER = OrganizationSchema
#     LINKS = {
#         'organizations': {
#             'responder': OrganizationResponder
#         }
#     }


# class UsersSharedInterestsResponder(Responder):
#     TYPE = 'user'
#     SERIALIZER = UserSchema
#     LINKS = UserResponder.LINKS
#

# GroupResponder.LINKS = {
#     'interests': {
#         'responder': InterestResponder,
#         'href': '%s/groups/{groups.id}/interests/{interests.id}' % (settings.SITE_URL)
#     },
#     'goals': {
#         'responder': GoalResponder,
#         'href': '%s/groups/{groups.id}/goals/{goals.id}' % (settings.SITE_URL)
#     },
#     'users': {
#         'responder': UserResponder,
#         'href': '%s/users/{users.id}' % (settings.SITE_URL)
#     }
# }

# UserResponder.LINKS = {
#     'interests': {
#         'responder': InterestResponder,
#         'href': '%s/users/{users.id}/interests/{interest.id}' % (settings.SITE_URL)
#
#     },
#     'groups': {
#         'responder': GroupResponder,
#         'href': '%s/users/{users.id}/groups/{group.id}' % (settings.SITE_URL)
#     },
#     'locations': {
#         'responder': LocationResponder,
#         'href': '%s/users/{users.id}/locations/{location.id}' % (settings.SITE_URL)
#     },
#     'goals': {
#         'responder': GoalResponder,
#         'href': '%s/users/{users.id}/goals/{goal.id}' % (settings.SITE_URL)
#     },
#     'organizations': {
#         'responder': OrganizationResponder,
#         'href': '%s/organizations/{organization.id}' % (settings.SITE_URL)
#     }
# }



#
# class SingleResponder(Responder):
#     TYPE = None
#
#     def __init__(self):
#         super(SingleResponder, self).__init__()
#         self.root = self.TYPE


