import smtplib
import ssl
from typing import Iterable, Text
import os


def send_email(receivers: Iterable[str], message: Text) -> None:
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender = os.environ["SENDER_EMAIL"]
    password = os.environ["SENDER_EMAIL_PASSWORD"]
    message = message
    context = ssl.create_default_context()

    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=context)
        server.login(sender, password)
        for receiver in receivers:
            server.sendmail(sender, receiver, message)
