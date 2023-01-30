


import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import datetime
## FILE TO SEND AND ITS PATH
filename = 'report.html'
SourcePathName  = 'D:/a/r1/a/'+filename
print(SourcePathName)
msg = MIMEMultipart()
msg['From'] = 'rahulrnr173@gmail.com'
msg['To'] = 'raghuln@nallas.com'
msg['Subject'] = ' SAMPLE REPORT '+str(datetime.datetime.now())
body = 'Please find the attachment for the Detailed Report'
msg.attach(MIMEText(body, 'plain'))

## ATTACHMENT PART OF THE CODE IS HERE
attachment = open(SourcePathName, 'rb')
part = MIMEBase('application', "octet-stream")
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
msg.attach(part)


session = smtplib.SMTP('smtp.gmail.com', 587)
session.starttls()
session.login("rahulrnr173@gmail.com", 'dtrkwzssutnbiwmk')
session.sendmail('rahulrnr173@gmail.com', 'raghuln@nallas.com', msg.as_string())
session.quit()
print('Mail Sent')


