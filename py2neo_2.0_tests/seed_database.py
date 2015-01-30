__author__ = 'Marnee Dearman'
from agora_db.py2neo_user import AgoraUser
from agora_db.py2neo_interest import AgoraInterest
from agora_db.agora_types import AgoraLabel, AgoraRelationship
from agora_db.py2neo_group import AgoraGroup
from agora_db.py2neo_location import AgoraLocation
from agora_db.py2neo_goal import AgoraGoal
from agora_db.py2neo_organization import AgoraOrganization
import datetime
from py2neo import Graph

Graph().delete_all()

#locations
tucson = AgoraLocation()
tucson.name = 'Tucson'
tucson.formatted_address = 'Tucson, AZ, USA'
tucson.place_id = 'ChIJK-0sC0Fl1oYRFccWTTgtw3M'
tucson.create_location()

bisbee = AgoraLocation()
bisbee.name = 'Bisbee'
bisbee.formatted_address = 'Bisbee, AZ 85603, USA'
bisbee.place_id = 'ChIJL9jhHLi00IYRGms2fEz_zGU'
bisbee.create_location()

#INTERESTS
#Kettlebells, Internet Startup, Python Programming
interest = AgoraInterest()
interest.name = 'Kettlebells'
interest.description = 'Getting strong with those cannonballs with handles'
interest.create_interest()
kettlebells_id = interest.id

interest = AgoraInterest()
interest.name = 'Internet Startup'
interest.description = 'How to build an Internet business'
interest.create_interest()
startup_id = interest.id

interest = AgoraInterest()
interest.name = 'Python Programming'
interest.description = 'Programming with the Python language'
interest.create_interest()
python_id = interest.id


#USERS
#Marnee, Julian, Chris, Dan, Megan, Liz, Frank
marnee = AgoraUser()
marnee.email = 'marnee@agorasociety.com'
marnee.name = 'Marnee'
marnee.is_admin = True
marnee.about = 'This is about me.'
marnee.mission_statement = 'This is my mission statement.'
marnee.create_user()

julian = AgoraUser()
julian.email = 'julian@agorasociety.com'
julian.name = 'Julian'
julian.is_admin = False
julian.about = 'This is about me.'
julian.mission_statement = 'This is my mission statement.'
julian.create_user()

chris = AgoraUser()
chris.email = 'chris@agorasociety.com'
chris.name = 'Chris'
chris.is_admin = True
chris.about = 'This is about me.'
chris.mission_statement = 'This is my mission statement.'
chris.create_user()

dan = AgoraUser()
dan.email = 'dan@agorasociety.com'
dan.name = 'Dan'
dan.is_admin = False
dan.about = 'This is about me.'
dan.mission_statement = 'This is my mission statement.'
dan.create_user()

frank = AgoraUser()
frank.email = 'frank@agorasociety.com'
frank.name = 'Frank'
frank.is_admin = False
frank.about = 'This is about me.'
frank.mission_statement = 'This is my mission statement.'
frank.create_user()

liz = AgoraUser()
liz.email = 'liz@agorasociety.com'
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
marnee.add_interest(kettlebells_id, experience)
print marnee.user_interests
marnee.add_interest(startup_id, experience)
marnee.add_interest(python_id, experience)
marnee.add_location(tucson.place_id)

julian.add_interest(kettlebells_id, experience)
julian.add_interest(startup_id, experience)
julian.add_interest(python_id, experience)
julian.add_location(tucson.place_id)

chris.add_interest(startup_id, experience)
chris.add_location(tucson.place_id)

dan.add_interest(startup_id, experience)
dan.add_location(tucson.place_id)

frank.add_interest(startup_id, experience)
frank.add_interest(python_id, experience)
frank.add_location(tucson.place_id)

liz.add_interest(startup_id, experience)
liz.add_location(tucson.place_id)

#groups
demo_day = AgoraGroup()
demo_day.about = 'Demo your progress and talk about your startup'
demo_day.mission_statement = 'Mission statement.'
demo_day.name = 'Tucson Startup Demo Day'
demo_day.meeting_location = 'Tucson Co-Lab'
demo_day.website = 'http://www.www.com'
demo_day.is_invite_only = True
demo_day.next_meeting_date = datetime.date.today()
demo_day.next_meeting_time = datetime.datetime.now().time()
demo_day.is_open = True
demo_day.create_group()

#add interests to group
demo_day.add_interest(startup_id)

#add users to group

marnee.join_group(demo_day.id)
julian.join_group(demo_day.id)
dan.join_group(demo_day.id)
chris.join_group(demo_day.id)
frank.join_group(demo_day.id)
liz.join_group(demo_day.id)

marnee_goal = AgoraGoal()
marnee_goal.title = 'Launch the Agora startup.'
marnee_goal.description = 'Make app public and get users.'
marnee_goal.start_date = datetime.date.today()
marnee_goal.end_date = datetime.date.today() + datetime.timedelta(days=400)
marnee_goal.create_goal()

marnee_goal.add_interest(startup_id)

marnee.add_goal(marnee_goal.id)
# julian.add_goal(goal.id)
# dan.add_goal(goal.id)
# chris.add_goal(goal.id)
# frank.add_goal(goal.id)

print marnee.get_local_users_shared_interests_near_location()

#organization
evo_fit = AgoraOrganization()
evo_fit.name = 'Evolution Fitness Tucson'
evo_fit.about = "Tucson's School of Strength: Personal Training, Kettlebells, Olympic Lifting, Kettlebell Training for women, Personal Trainers Tucson, Powerlifting"
evo_fit.email = 'info@evolutionfitness.com'
evo_fit.is_invite_only = True
evo_fit.is_open = True
evo_fit.mission_statement = 'Get Tucson fit, strong, and healthy.'
evo_fit.website = 'http://www.evolutiontucson.com/'
evo_fit.create_organization()

#add interests
evo_fit.add_interest(kettlebells_id)

#add users to organization
marnee.join_organization(evo_fit.id)
julian.join_organization(evo_fit.id)
