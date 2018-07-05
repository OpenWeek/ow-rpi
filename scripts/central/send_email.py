import traceback
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header


def get_config():
  with open("../../config/sendEmail.yaml", 'r') as stream:
    try:
      return yaml.safe_load(stream)
    except yaml.YAMLError as exc:
      print(exc)

def send_mail(subject, text):
  try:
    config = get_config()
    smtpserver = smtplib.SMTP(config['SMTP_SERVER'], config['SMTP_PORT'])
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(config['MAIL_USER'], config['MAIL_PASS'])
    header = u'ALARM From: ' + config['MAIL_USER']
    header = header + '\t' + u'Subject:' + subject + u'\n'

    msg = MIMEMultipart('alternative')
    msg.set_charset('utf8')
    msg['From'] = config['MAIL_USER']
    msg['To'] = config['MAIL_RECIPIENT']
    msg['Subject'] = Header(
        subject.encode('utf-8'),
        'UTF-8'
    ).encode()

    _attach = MIMEText(text.encode('utf-8'), 'plain', 'UTF-8')
    msg.attach(_attach)
    print msg.as_string()

    smtpserver.sendmail(config['MAIL_USER'], config['MAIL_RECIPIENT'], msg.as_string())
    smtpserver.close()
    print "DONE"
    return True
  except:
    traceback.print_exc()
    return False

send_mail("subject", "text message")
