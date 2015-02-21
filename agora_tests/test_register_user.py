__author__ = 'Marnee Dearman'
import sys, os
from agora_db import user

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

email = 'marnee.dearman@gmail.com'

recipients = []
recipients.append(email)
print ", ".join(recipients)

reg_user = user.AgoraUser()
reg_user.register_user(email)

