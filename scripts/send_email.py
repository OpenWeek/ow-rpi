import traceback
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header

GMAIL_USER = 'ow-rpi@gmx.fr'
GMAIL_Recipient=''
GMAIL_PASS = ''
SMTP_SERVER = 'mail.gmx.com'
SMTP_PORT = 587

def send_mail(subject, text):
  try:
    smtpserver = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(GMAIL_USER, GMAIL_PASS)
    header = u'ALARM From: ' + GMAIL_USER
    header = header + '\t' + u'Subject:' + subject + u'\n'

    msg = MIMEMultipart('alternative')
    msg.set_charset('utf8')
    msg['From'] = GMAIL_USER
    msg['To'] = GMAIL_Recipient
    msg['Subject'] = Header(
        subject.encode('utf-8'),
        'UTF-8'
    ).encode()

    _attach = MIMEText(text.encode('utf-8'), 'plain', 'UTF-8')
    msg.attach(_attach)
    print msg.as_string()

    smtpserver.sendmail(GMAIL_USER, GMAIL_Recipient, msg.as_string())
    smtpserver.close()
    print "DONE"
    return True
  except:
    traceback.print_exc()
    return False


