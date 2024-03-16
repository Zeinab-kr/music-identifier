import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from initials import gmail_user, gmail_password


def send_email(to_email, subject, message):
    msg = MIMEMultipart()
    msg['From'] = gmail_user
    msg['To'] = to_email
    msg['Subject'] = subject

    body = message
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(gmail_user, gmail_password)
        server.sendmail(gmail_user, to_email, msg.as_string())
        server.close()
        print("Email sent successfully to:", to_email)
    except Exception as e:
        print("Failed to send email:", str(e))
