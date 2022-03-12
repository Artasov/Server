# -*- coding: utf-8 -*-

import environ
from smtplib import SMTP_SSL, SMTP, SMTPAuthenticationError
import time
from ssl import create_default_context
from email.message import EmailMessage, Message

alphabet = {
    'en': '',
    'ru': ''
}


def open_write(path, text, printing=False, encoding='utf-8'):
    open(path, 'w', encoding=encoding).write(text)
    if printing:  print(open(path, 'r', encoding=encoding).read())


def open_append(path, text, printing=False, encoding='utf-8'):
    open(path, 'a', encoding=encoding).write(text)
    if printing:  print(open(path, 'r', encoding=encoding).read())


def open_prepend(path, text, printing=False, encoding='utf-8'):
    text = text + open(path, 'r', encoding=encoding).read()
    open(path, 'w', encoding=encoding).write(text)
    if printing:  print(open(path, 'r', encoding=encoding).read())


def random_str(length=10, alphabet='abcdefghijklmnopqrstuvwxyz1234567890', repete=True, upper=True):  # ru #digits
    import random

    if repete:
        rand_str = ''.join(random.choice(alphabet) for i in range(length))
    else:
        try:
            rand_str = ''.join(random.sample(alphabet, length))
        except ValueError:
            raise ValueError(
                "The alphabet is less than the length of the string. Generation without repetition is impossible.")
    if upper:
        return rand_str.upper()
    else:
        return rand_str


def send_EMail(port: int, to: str, subject: str, html: str):
    env = environ.Env()
    server = 'smtp.timeweb.ru'
    user = env('EMAIL_HOST_USER')
    password = env('EMAIL_HOST_PASSWORD')

    import smtplib
    import os
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders
    from platform import python_version

    sender = user
    subject = subject
    text = 'Something go wrong'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = to
    msg['Reply-To'] = sender
    msg['Return-Path'] = sender
    msg['X-Mailer'] = 'Python/' + (python_version())

    part_text = MIMEText(text, 'plain')
    part_html = MIMEText(html, 'html')

    msg.attach(part_text)
    msg.attach(part_html)

    mail = smtplib.SMTP_SSL(server)
    mail.login(user, password)
    mail.sendmail(sender, to, msg.as_string())
    mail.quit()
