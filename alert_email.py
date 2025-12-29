import smtplib
from email.mime.text import MIMEText

def send_email(subject, body, cfg):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = cfg.EMAIL_USER
    msg["To"] = cfg.EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(cfg.EMAIL_USER, cfg.EMAIL_PASS)
        server.send_message(msg)
