__author__ = 'Marnee Dearman'
from marshmallow import Schema, fields
from hyp.marshmallow import Responder


class UserSchema(Schema):
    id = fields.String()
    name = fields.String()
    email = fields.String()
    mission_statement = fields.String()
    is_mentor = fields.Boolean()
    is_tutor = fields.Boolean()
    is_visible = fields.Boolean()
    is_available = fields.Boolean()
    is_admin = fields.Boolean()
    # interests = fields.List(fields.String)
    # goals = fields.List(fields.String)
    # locations = fields.List(fields.String)
    # groups = fields.List(fields.String)
    # organizations = fields.List(fields.String)


class UserProfileSchema(Schema):
    id = fields.String()
    name = fields.String()
    email = fields.String()
    mission_statement = fields.String()
    is_mentor = fields.Boolean()
    is_tutor = fields.Boolean()
    is_visible = fields.Boolean()
    is_available = fields.Boolean()
    is_admin = fields.Boolean()
    about = fields.String()
    permanent_web_token = fields.String()


class UsersSharedInterestsSchema(Schema):
    id = fields.String()
    email = fields.String()
    interests_users = fields.String()


class UserInterestSchema(Schema):
    id = fields.String()
    email = fields.String()
    # interests = fields.String()
    # InterestSchema(Schema)        #fields.List(fields.String)


class InterestSchema(Schema):
    # interests = fields.List(fields)
    name = fields.String()
    id = fields.String()
    experience = fields.String()
    time = fields.String()


# class SharedInterstsSchems(Schema):
# interests_users = fields.String()


class UserGoalsSchema(Schema):
    id = fields.String()
    email = fields.String()


class GoalSchema(Schema):
    id = fields.String()
    title = fields.String()
    description = fields.String()
    start_date = fields.String()
    end_date = fields.String()
    created_date = fields.String()
    is_public = fields.String()
    # interests = fields.List(fields.String())


class GoalInterestSchema(Schema):
    id = fields.String()
    goal_id = fields.String()
    name = fields.String()


class GroupSchema(Schema):
    id = fields.String()
    name = fields.String()
    description = fields.String()
    is_open = fields.Boolean()
    is_invite_only = fields.Boolean()
    meeting_location = fields.String()
    next_meeting_date = fields.Date()
    next_meeting_time = fields.String()
    interests = fields.List(fields.String())


class UserGroupsSchema(Schema):
    id = fields.String()
    email = fields.String()
    # groups = fields.List(fields.String)


class OrganizationSchema(Schema):
    id = fields.String()
    name = fields.String()
    mission_statement = fields.String()
    about = fields.String()
    email = fields.String()
    is_open = fields.String()
    is_invite_only = fields.String()
    website = fields.String()
    interests = fields.List(fields.String())


class UserOrganizationSchema(Schema):
    id = fields.String()
    email = fields.String()


class UserLocationsSchema(Schema):
    id = fields.String()
    email = fields.String()
    # locations = fields.List(fields.String)


class LocationSchema(Schema):
    id = fields.String()
    name = fields.String()
    formatted_address = fields.String()


class ActivatedUserSchema(Schema):
    id = fields.String()
    permanent_web_token = fields.String()


class SingleResponder(Responder):
    TYPE = None

    def __init__(self):
        super(SingleResponder, self).__init__()
        self.root = self.TYPE


class ActivatedUserResponder(Responder):
    TYPE = 'user'
    SERIALIZER = ActivatedUserSchema


class UserProfileResponder(Responder):
    TYPE = 'user'
    SERIALIZER = UserProfileSchema


class InterestResponder(Responder):
    TYPE = 'interests'
    SERIALIZER = InterestSchema


class UserInterestResponder(Responder):
    TYPE = 'user'
    SERIALIZER = UserInterestSchema
    LINKS = {
        'interests': {
            'responder': InterestResponder,
            'href': 'http://localhost:8000/interests/{interests.id}'
        }
    }


class GoalResponder(Responder):
    TYPE = 'goals'
    SERIALIZER = GoalSchema
    LINKS = {
        'interests': {
            'responder': InterestResponder,
            'href': 'http://localhost:8000/interests/{interests.id}'
        }
    }


class GoalInterestResponder(Responder):
    TYPE = 'interests'
    SERIALIZER = GoalInterestSchema


class UserGoalsResponder(Responder):
    TYPE = 'user'
    SERIALIZER = UserGoalsSchema
    LINKS = {
        'goals': {
            'responder': GoalResponder,
            'href': 'http://localhost:8000/users/{user.email}/goals/{goal.id}'
        }
    }


class UserLocationsResponder(Responder):
    TYPE = 'user'
    SERIALIZER = UserLocationsSchema


class UserSharedInterestsResponder(Responder):
    TYPE = 'user'
    SERIALIZER = UsersSharedInterestsSchema


class GroupResponder(Responder):
    TYPE = 'groups'
    SERIALIZER = GroupSchema
    # LINKS = {
    # 'interests': InterestResponder,
    # 'users': UserResponder
    # }


class LocationResponder(Responder):
    TYPE = 'locations'
    SERIALIZER = LocationSchema


class UserGroupsResponder(Responder):
    TYPE = 'user'
    SERIALIZER = UserGroupsSchema
    LINKS = {
        'groups': {
            'responder': GroupResponder
        },
    }


class OrganizationResponder(Responder):
    TYPE = 'organizations'
    SERIALIZER = OrganizationSchema


class UserOrganizationsResponder(Responder):
    TYPE = 'users'
    SERIALIZER = OrganizationSchema
    LINKS = {
        'organizations': {
            'responder': OrganizationResponder
        }
    }


class UserResponder(Responder):
    TYPE = 'user'
    SERIALIZER = UserSchema


GroupResponder.LINKS = {
    'interests': {
        'responder': InterestResponder,
        'href': 'http://localhost:8000/interests/{interest.id}'
    },
    'users': {
        'responder': UserResponder,
        'href': 'http://localhost:8000/users/{user.email}'
    }
}

UserResponder.LINKS = {
    'interests': {
        'responder': InterestResponder,
        'href': 'http://localhost:8000/interests/{interest.id}'

    },
    'groups': {
        'responder': GroupResponder,
        'href': 'http://localhost:8000/groups/{group.id}'
    },
    'locations': {
        'responder': LocationResponder,
        'href': 'http://localhost:8000/locations/{location.id}'
    },
    'goals': {
        'responder': GoalResponder,
        'href': 'http://localhost:8000/goals/{goal.id}'
    },
    'organizations': {
        'responder': OrganizationResponder,
        'href': 'http://localhost:8000/organizations/{organization.id}'
    }
}


