import re
def extract_email_info(text):
    sender = re.search(r'From: (.*)', text)
    urgency = 'high' if 'urgent' in text.lower() else 'normal'
    return {
        "sender": sender.group(1) if sender else "Unknown",
        "urgency": urgency,
        "body": text
    }
