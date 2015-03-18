__author__ = 'Marnee Dearman'
from db.py2neo_user import AgoraUser
from db.py2neo_interest import AgoraInterest
import time
#get existing user
user = AgoraUser()
user.name = 'Marnee'
user.email = 'marnee@agorasociety.com'
user.get_user()

#update property on user
# user.mission_statement = "Learn all the things."
# user.update_user()

#update existing relationship to interest
# experience_properties_dict = {
#     'experience': 'Followed Enter the Kettlebell and used to go to Evolution Fitness, a kettlebell gym.',
#     'time': '4 years'
# }
# user.update_interest('794da45f-85a9-4ba9-a090-92598a799f9d', experience_properties_dict)
#
# #show user interests
# print user.user_interests
#
# #create user
# user = AgoraUser()
# user.email = 'megan@agorasociety.com'
# user.name = 'Megan'
# user.mission_statement = 'Learn all the things.'
# user.about = 'This is about me!'
# user.is_available_for_in_person = True
#
# user.create_user()
#
# #update property on new user
# user.about = 'All about Megan'
# user.update_user()
#
# #add interest to user
# #interest = Kettlebells =  794da45f-85a9-4ba9-a090-92598a799f9d
# experience_properties_dict = {
#     'experience': 'Beginner, following Enter the Kettlebell',
#     'time': '2 weeks'
# }
#
# user.add_interest('794da45f-85a9-4ba9-a090-92598a799f9d', experience_properties_dict)
# print user.user_interests
#
# #add goal to user
#

