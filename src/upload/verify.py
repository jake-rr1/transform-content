import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import date, timedelta
import base64
import re

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def get_verification_code() -> str:
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    
    # Dates have to formatted in YYYY/MM/DD format for gmail
    today = date.today()
    yesterday = today - timedelta(1)
    
    query = 'from:no-reply@verify.proton.me, newer_than:10h +Verification, is:unread'
    
    results = service.users().messages().list(userId="me", labelIds=["INBOX"], q=query, maxResults=1).execute()

    messages = results.get("messages", [])
    
    if results['resultSizeEstimate'] == 0:
        return ''
    
    message_count = 0
    for message in messages:
        msg = service.users().messages().get(userId="me", id=message["id"]).execute()
        message_count = message_count + 1
        email_data = msg["payload"]["headers"]
        for values in email_data:
            name = values["name"]
            if name == "From":
                from_name = values["value"]
                subject = [j["value"] for j in email_data if j["name"] == "Subject"]
                
        # I added the below script.
        for p in msg["payload"]["parts"]:
            if p["mimeType"] in ["text/plain", "text/html"]:
                data = base64.urlsafe_b64decode(p["body"]["data"]).decode("utf-8")
    
    match = re.search(r'<code style="font-size: 2.5em; line-height: 2em;">(.*?)</code>', data)
    if match:
        verification_code = match.group(1)
    
    return str(verification_code)
    
  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")
