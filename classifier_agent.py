import json

def detect_format(data, filename=None):
    if filename and filename.lower().endswith('.pdf'):
        return 'PDF'
    try:
        json.loads(data)
        return 'JSON'
    except:
        return 'EMAIL'

def detect_intent(text):
    text = text.lower()
    if 'invoice' in text: return 'Invoice'
    if 'rfq' in text or 'request for quotation' in text: return 'RFQ'
    if 'complaint' in text: return 'Complaint'
    if 'regulation' in text: return 'Regulation'
    return 'Unknown'
