__author__ = 'Marnee Dearman'
from agora_services.smtp import AgoraSmtp

test_mail = AgoraSmtp()
#use the defaults
recipient_list = ['marnee.dearman@gmail.com']
test_mail.recipients = recipient_list
test_mail.sender = 'agora.dev.testing@gmail.com'
test_mail.send_by_gmail()

