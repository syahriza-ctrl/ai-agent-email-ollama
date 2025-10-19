from gmail.gmail_auth import gmail_login
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
def get(after_str: str):
    service = gmail_login()

    results =  service.users().messages().list(
        userId='me',
        labelIds=["INBOX"],
        maxResults=25,
        q = f"after:{after_str}"
    ).execute()
    
    messages = results.get("messages",[])
    email_data = []

            
    for msg in messages:
        msg_id = msg['id']
        msg_detail = service.users().messages().get(
            userId='me', 
            id=msg_id, 
            format='metadata',  # cukup metadata agar lebih ringan
            metadataHeaders=['From']  # hanya ambil header 'From'
        ).execute()

        snippet = msg_detail.get('snippet', '')
        headers = msg_detail.get('payload', {}).get('headers', [])
        sender = ''
        for h in headers:
            if h['name'] == 'From':
                sender = h['value']
                break

        email_data.append({
            'from': sender,
            'snippet': snippet
        })

    return email_data