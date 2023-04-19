from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleDriveAPI:
    def __init__(self, credentials: Credentials):
        self.service = build('drive', 'v3', credentials=credentials)

    def list_files(self):
        try:
            files = []
            page_token = None
            while True:
                response = self.service.files().list(q="trashed = false", spaces='drive', fields='nextPageToken, '
                                                                                               'files(id, name, '
                                                                                               'mimeType, owners, '
                                                                                               'createdTime, '
                                                                                               'modifiedTime, '
                                                                                               'visibility)',
                                                     pageToken=page_token).execute()
                for file in response.get('files', []):
                    files.append(file)
                page_token = response.get('nextPageToken', None)
                if page_token is None:
                    break
            return files
        except HttpError as error:
            print(f'An error occurred: {error}')
            return []

    def make_file_private(self, file_id: str):
        try:
            file = self.service.files().get(fileId=file_id, fields='id, name, '
                                                                    'mimeType, owners, createdTime, '
                                                                    'modifiedTime, visibility').execute()

            if file['visibility'] == 'anyoneCanView':
                file['visibility'] = 'private'
                updated_file = self.service.files().update(fileId=file['id'], body=file, fields='id, name, '
                                                                                                  'mimeType, owners, '
                                                                                                  'createdTime, '
                                                                                                  'modifiedTime, '
                                                                                                  'visibility').execute()
                return updated_file
        except HttpError as error:
            print(f'An error occurred: {error}')
            return None