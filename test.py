from __future__ import print_function
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from httplib2 import Http
from oauth2client import file, client, tools
import io

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/drive'

store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('drive', 'v2', http=creds.authorize(Http()))

def download(file_id, mimeType, filename):
    #file_id = '1x1xfXabp9Mmg2zsbprTOGAgm9TIbtAPT'
    request = service.files().get_media(fileId=file_id)
    fh = io.FileIO(filename,'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()
        print ("Download %d%%. " % int(status.progress() * 100))

def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """


    # Call the Drive v3 API
    folderId = '1qsUk6ibc5rsi-mO9sShYcPgTopRPBBfv'
    results = service.children().list(folderId=folderId).execute()
    items = results.get('items', [])

    if not items:
        print('No files found.')
    else:
        print('Files:')
        #file_id = '0B5Oj9nyOz4ahenNETHFZaFZHNlE'


            
        for item in items:
            #print(item)
            file = service.files().get(fileId=item['id']).execute()
            print(file['title'], "  ", file['id'], " ", file['mimeType'])
            download(file['id'],file['mimeType'],filename=folderId+"."+file['title'])

if __name__ == '__main__':
    main()
