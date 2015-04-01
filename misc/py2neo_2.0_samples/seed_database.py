__author__ = 'Marnee Dearman'
from db.user import User
from db.interest import Interest
from db.labels_relationships import GraphLabel, GraphRelationship
from db.group import Group
from db.location import Location
from db.goal import Goal
from db.organization import Organization
import datetime
import settings
from py2neo import Graph

print Graph(settings.DATABASE_URL).neo4j_version

Graph(settings.DATABASE_URL).delete_all()

#locations
tucson = Location()
tucson.name = 'Tucson'
tucson.formatted_address = 'Tucson, AZ, USA'
tucson.id = 'ChIJK-0sC0Fl1oYRFccWTTgtw3M'
tucson.create_location()

tucson_json = {
    "location": {
        "id": "ChIJK-0sC0Fl1oYRFccWTTgtw3M",
        "name": "Tucson",
        "formatted_address": "Tucson, AZ, USA"
    }
}

bisbee = Location()
bisbee.name = 'Bisbee'
bisbee.formatted_address = 'Bisbee, AZ 85603, USA'
bisbee.id = 'ChIJL9jhHLi00IYRGms2fEz_zGU'
bisbee.create_location()

#INTERESTS
#Kettlebells, Internet Startup, Python Programming
interest = Interest()
interest.name = 'Amateur Radio'
interest.description = 'Getting strong with those cannonballs with handles'
interest.create_interest()
amateur_radio_id = interest.id

interest = Interest()
interest.name = 'Motorcyles'
interest.create_interest()
interest_moto_id = interest.id

interest = Interest()
interest.name = 'Cooking'
interest.create_interest()
cooking_id = interest.id

interest = Interest()
interest.name = 'Internet Startup'
interest.description = 'How to build an Internet business'
interest.create_interest()
startup_id = interest.id

interest = Interest()
interest.name = 'Python Programming'
interest.description = 'Programming with the Python language'
interest.create_interest()
python_id = interest.id


#USERS
#Marnee, Julian, Chris, Dan, Liz, Frank
marnee = User()
marnee.call_sign = 'AWESOME'
marnee.email = 'marnee@elmerly.com'
marnee.name = 'Marnee'
marnee.is_admin = True
marnee.about = 'This is about me.'
marnee.mission_statement = 'This is my mission statement.'
marnee.create_user()

julian = User()
julian.call_sign = 'RADICAL'
julian.email = 'julian@elmerly.com'
julian.name = 'Julian'
julian.is_admin = False
julian.about = 'This is about me.'
julian.mission_statement = 'This is my mission statement.'
julian.create_user()

chris = User()
chris.email = 'chris@elmerly.com'
chris.name = 'Chris'
chris.is_admin = True
chris.about = 'This is about me.'
chris.mission_statement = 'This is my mission statement.'
chris.create_user()

dan = User()
dan.email = 'dan@elmerly.com'
dan.name = 'Dan'
dan.is_admin = False
dan.about = 'This is about me.'
dan.mission_statement = 'This is my mission statement.'
dan.create_user()

frank = User()
frank.email = 'frank@elmerly.com'
frank.name = 'Frank'
frank.is_admin = False
frank.about = 'This is about me.'
frank.mission_statement = 'This is my mission statement.'
frank.create_user()

liz = User()
liz.email = 'liz@elmerly.com'
liz.name = 'Liz'
liz.is_admin = False
liz.about = 'This is about me.'
liz.mission_statement = 'This is my mission statement.'
liz.create_user()

experience = {
    'experience': 'This is my experience desc.',
    'time': '100 years'
}

#link to interests and locations
marnee.add_interest(amateur_radio_id, experience)
# print marnee.user_interests
marnee.add_interest(startup_id, experience)
marnee.add_interest(python_id, experience)
marnee.add_location(tucson_json['location'])

julian.add_interest(amateur_radio_id, experience)
julian.add_interest(startup_id, experience)
julian.add_interest(python_id, experience)
julian.add_interest(interest_moto_id, experience)
julian.add_location(tucson_json['location'])

chris.add_interest(startup_id, experience)
chris.add_interest(cooking_id, experience)
chris.add_interest(amateur_radio_id, experience)
chris.add_location(tucson_json['location'])

dan.add_interest(startup_id, experience)
dan.add_location(tucson_json['location'])

frank.add_interest(startup_id, experience)
frank.add_interest(python_id, experience)
frank.add_interest(amateur_radio_id, experience)
frank.add_interest(cooking_id, experience)
frank.add_location(tucson_json['location'])

liz.add_interest(startup_id, experience)
liz.add_location(tucson_json['location'])

#groups
# demo_day = Group()
# demo_day.about = 'Demo your progress and talk about your startup'
# demo_day.mission_statement = 'Mission statement.'
# demo_day.name = 'Tucson Startup Demo Day'
# demo_day.meeting_location = 'Tucson Co-Lab'
# demo_day.website = 'http://www.www.com'
# demo_day.is_invite_only = True
# demo_day.next_meeting_date = datetime.date.today()
# demo_day.next_meeting_time = datetime.datetime.now().time()
# demo_day.is_open = True
# demo_day.create_group()

#add interests to group
# demo_day.add_interest(startup_id)

#add users to group

# marnee.join_group(demo_day.id)
# julian.join_group(demo_day.id)
# dan.join_group(demo_day.id)
# chris.join_group(demo_day.id)
# frank.join_group(demo_day.id)
# liz.join_group(demo_day.id)

# marnee_goal = Goal()
# marnee_goal.title = 'Launch the Elmerly startup.'
# marnee_goal.description = 'Make app public and get users.'
# marnee_goal.start_date = datetime.date.today()
# marnee_goal.end_date = datetime.date.today() + datetime.timedelta(days=400)
# marnee_goal.create_goal()
#
# marnee_goal.add_interest(startup_id)
# marnee.add_goal(marnee_goal.id)

# julian.add_goal(goal.id)
# dan.add_goal(goal.id)
# chris.add_goal(goal.id)
# frank.add_goal(goal.id)

# print marnee.get_local_users_shared_interests_near_location()

#organization
ovarc = Organization()
ovarc.name = 'Oro Valley Amateur Radio Club'
ovarc.about = 'Oro Valley Amateur Radio Club'
ovarc.email = 'club@elmerly.com'
ovarc.is_invite_only = True
ovarc.is_open = True
ovarc.mission_statement = 'Advance amateur radio in southern arizona'
ovarc.website = 'http://www.com'
ovarc.create_organization()

#add interests
ovarc.add_interest(amateur_radio_id)

#add users to organization
marnee.join_organization(ovarc.id)
julian.join_organization(ovarc.id)
