__author__ = 'Marnee Dearman'
from agora_services.smtp import AgoraSmtp

test_mail = AgoraSmtp()
# test_mail.su
recipient_list = ['marnee.dearman@gmail.com', 'agora.dev.testing@gmail.com']
test_mail.recipients = recipient_list
test_mail.sender = 'agora.dev.testing@gmail.com'
# test_mail.message = 'TESTING HELLO FROM THE AGORAAAA!!!!'
test_mail.send_by_gmail()

