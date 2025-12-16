import os
from .telegram_notifier import TelegramNotifier
from .sms_notifier import SMSNotifier
from .email_notifier import EmailNotifier

# Initialize global notifiers based on env (legacy support) or dynamic per-user
# This module acts as a factory or holder for shared notifier logic

def get_telegram_notifier(token, chat_id):
    if token and chat_id:
        return TelegramNotifier(token, chat_id)
    return None

def get_email_notifier(host, port, sender, password, recipient):
    return EmailNotifier(host, port, sender, password, recipient)

def get_sms_notifier(api_key):
    return SMSNotifier(api_key)
