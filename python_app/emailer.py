import smtplib

from email.mime.text import MIMEText


def send_email(content: str, subject: str, reciever: str):
    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['From'] = "no-reply@myproject.com"
    msg['To'] = reciever

    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()
