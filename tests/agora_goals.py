__author__ = 'Marnee Dearman'
from db.py2neo_goal import AgoraGoal
from db.py2neo_user import AgoraUser
from db.py2neo_interest import AgoraInterest
from datetime import date, datetime, timedelta

#create a goal
new_goal = AgoraGoal()
new_goal.title = 'Kettlebell Swing'
new_goal.description = '100 50 lb. kettlebells swings.'
new_goal.start_date = date.today()
new_goal.end_date = date.today() + timedelta(days=180)
new_goal.create_goal()

#Add goal to user
user = AgoraUser()
user.email = 'marnee@agorasociety.com'
user.get_user()
user.add_goal(new_goal.id)

#update goal
goal = AgoraGoal()
goal.id = new_goal.id
goal.get_goal()
goal.title = 'Master Russian Kettlebell Swing'
goal.update_goal()

#link goal to interests
#kettlebells '794da45f-85a9-4ba9-a090-92598a799f9d'
goal.add_interest('a7d03c1c-58fa-4bd4-8f00-ce45aa312a5c')

#delete if running test over and over like I am
# user.delete_goal(goal.id)
