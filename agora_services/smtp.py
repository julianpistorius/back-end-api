__author__ = 'Marnee Dearman'
# Import smtplib for the actual sending function
import smtplib
from email.mime.text import MIMEText
from email.parser import Parser
# Import the email modules we'll need
from email.mime.text import MIMEText

class AgoraSmtp(object):
    def __init__(self):
        self.recipients = []
        self.sender = 'agora.dev.testing@gmail.com'
        self.message = 'WELCOME TO THE AGORA'
        self.subject = 'TESTING NOTIFICATIONS'
        self.html_file = None
        self.url = None
        # self.server
        # self.port

    def send_by_gmail(self):
        # Credentials (if needed)
        #TODO put in config file?
        username = 'agora.dev.testing@gmail.com'
        password = 'b~}.82yK;Zr&'

        #  If the e-mail headers are in a file, uncomment this line:
        #headers = Parser().parse(open(messagefile, 'r'))

        #  Or for parsing headers in a string, use:
        # headers = Parser().parsestr('From: <agora.dev.testing@gmail.com>\n'
        #         'To: <marnee.dearman@gmail.com>\n'
        #         'Subject: Test message\n'
        #         '\n'
        #         'Body would go here\n')

        #  Now the header items can be accessed as a dictionary:
        # print 'To: %s' % headers['to']
        # print 'From: %s' % headers['from']
        # print 'Subject: %s' % headers['subject']

        # The actual mail send
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login(username, password)
        msg = "\r\n".join([
        "From: " + self.sender,
        "To: " + ", ".join(self.recipients),
        "Subject: " + self.subject,
        "",
        self.message,
        self.url
        ])
        print msg
        server.sendmail(self.sender, self.recipients, msg)
        server.quit()



    # # Open a plain text file for reading.  For this example, assume that
    # # the text file contains only ASCII characters.
    # fp = open(textfile, 'rb')
    # # Create a text/plain message
    # msg = MIMEText(fp.read())
    # fp.close()
    #
    # # me == the sender's email address
    # # you == the recipient's email address
    # msg['Subject'] = 'The contents of %s' % textfile
    # msg['From'] = me
    # msg['To'] = you
    #
    # # Send the message via our own SMTP server, but don't include the
    # # envelope header.
    # s = smtplib.SMTP('localhost')
    # s.sendmail(me, [you], msg.as_string())
    # s.quit()
