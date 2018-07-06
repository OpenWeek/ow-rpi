# Openweek Raspberry pi's weather station
# Copyright c 2018  Maxime Postaire, Lucas Ody, Maxime Franco,
# Nicolas Rybowski, Benjamin De Cnuydt, Quentin Delmelle, Colin Evrard,
# Antoine Vanderschueren.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import traceback
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import yaml

def get_config():
  with open("ow_rpi/config/send_email.yaml", 'r') as stream:
    try:
      data = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
      print(exc)

    if 'MAIL_USER' not in data:
      data['MAIL_USER'] = "ow-rpi@gmx.fr"

    if 'MAIL_RECIPIENT' not in data:
      data['MAIL_RECIPIENT'] = "archein.lol@gmail.com"

    if 'MAIL_PASS' not in data:
      data['MAIL_PASS'] = ""

    if 'SMTP_SERVER' not in data:
      data['SMTP_SERVER'] = "mail.gmx.com"

    if 'SMTP_PORT' not in data:
      data['SMTP_PORT'] = 587

    return data


def send_mail(subject, text, mail_address = None):
	try:
		config = get_config()
		if mail_address == None:
			mail_address = []
			mail_address.append(config['MAIL_RECIPIENT'])
		smtpserver = smtplib.SMTP(config['SMTP_SERVER'], config['SMTP_PORT'])
		smtpserver.ehlo()
		smtpserver.starttls()
		smtpserver.ehlo
		smtpserver.login(config['MAIL_USER'], config['MAIL_PASS'])
		for mail in mail_address:
			msg = MIMEMultipart('alternative')
			msg.set_charset('utf8')
			msg['From'] = config['MAIL_USER']
			msg['To'] = mail
			msg['Subject'] = Header(
				subject.encode('utf-8'),
				'UTF-8'
			).encode()
			_attach = MIMEText(text.encode('utf-8'), 'plain', 'UTF-8')
			msg.attach(_attach)
			print msg.as_string()
			smtpserver.sendmail(config['MAIL_USER'], mail, msg.as_string())
		smtpserver.close()
		print "DONE"
		return True
	except:
		traceback.print_exc()
		return False
	

