import smtplib
from email.mime.text import MIMEText
import environment_data as env



def sendmail_success(subject,text):
    print("Now sending mail....")
    msg = MIMEText(text)
    msg['Subject'] = subject
    msg['From'] = env.DESTINATION_MAIL
    msg['To'] = env.DESTINATION_MAIL
    s = smtplib.SMTP(env.MAIL_SERVER)
    s.sendmail(msg['To'], [msg['From']], msg.as_string())
    s.quit()
    print("Mail sent")


