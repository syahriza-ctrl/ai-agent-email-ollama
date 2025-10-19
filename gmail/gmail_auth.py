import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scope menentukan izin yang kamu minta dari Gmail API
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def gmail_login():
    """Login ke Gmail API dan kembalikan service"""
    creds = None

    # Jika sudah pernah login, token.json akan menyimpan aksesnya
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    # Jika belum ada token, login manual pakai browser
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Simpan token agar tidak login ulang setiap kali
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # Bangun service Gmail API
    service = build("gmail", "v1", credentials=creds)
    return service
