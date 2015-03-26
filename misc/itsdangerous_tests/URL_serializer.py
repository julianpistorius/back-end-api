__author__ = 'Marnee Dearman'
from itsdangerous import URLSafeSerializer, URLSafeTimedSerializer, BadSignature, BadTimeSignature, TimestampSigner
import settings
import uuid
import time

#SERIALIZE FOR URL PAYLOAD
s = URLSafeSerializer(secret_key=settings.TOKEN_SECRET_KEY)
id = 'b808136d-148c-4206-8fa0-4cfa3eba6239'
payload = s.dumps(id)

# print s
print payload

#DESERLIZE
#and check time stamp

time.sleep(5)

try:
    id2 = s.loads(payload)  #, max_age=6)
    print id, id2
except BadTimeSignature:
    print 'out of time'

print settings.SITE_URL + "/%s" % payload

# except BadSignature:
#     print 'bad signature'

 # s = URLSafeTimedSerializer(secret_key=settings.TOKEN_SECRET_KEY)
 #        id = s.loads(payload, max_age=6000)

# if user.id == '':
            #send registration message

            #TODO do we need to store this?  It expires as defined above.  Should be good enough.
            # user.temporary_web_token = expiring_web_token
            #TODO setup message with URL and token
            # message.send_by_gmail()
            #if successful
            #do not create user until registration completed by email
            # user.create_user()
        # else:
        #     #send login message
            #TODO make a non-expiring web token??
            # permanent_web_token
        #     # user.permanent_web_token = web_token
        #     message.send_by_gmail()
        #     #if successful
        #     #do not update user until verification completed by email
        #     # user.update_user()