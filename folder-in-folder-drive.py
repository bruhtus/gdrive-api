import pickle
import os.path

from fire import Fire

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def main(name, folder_id):
    SCOPES = ['https://www.googleapis.com/auth/drive']

    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    drive_service = build('drive', 'v3', credentials=creds)

    folder_in_folder(name, folder_id, drive_service)

def folder_in_folder(name, folder_id, service):
    file_metadata = {
    'name' : name,
    'parents' : [folder_id],
    'mimeType' : 'application/vnd.google-apps.folder'
    }

    file = service.files().create(body=file_metadata,
                                    fields='id').execute()

    print ('Folder ID: %s' % file.get('id'))

if __name__ == '__main__':
    Fire(main)
