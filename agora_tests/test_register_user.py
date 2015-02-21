__author__ = 'Marnee Dearman'
import sys, os
from agora_db import user

myPath = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, myPath + '/../')

recipients = []
recipients.append("marnee.dearman@gmail.com")
print ", ".join(recipients)

reg_user = user.AgoraUser()
reg_user.register_user("marnee.dearman@gmail.com")

