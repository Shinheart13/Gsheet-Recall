from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('sheets', 'v4', credentials=creds)

    SPREADSHEET_ID = '133QoEZ2i5xkUMGgdDnPjahxUXv3Fr0zyo7wp4yGJEn4'
    RANGE_NAME = 'Sheet1!A:J'  # Adjust the range as needed
    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        # Print the header once
        header = values[0]  # Get the first row as header
        print(', '.join(header))  # Print the header

        # Iterate through rows starting from the second row
        for row in values[1:]:  # Skip the header row
            try:
                print('%s, %s, %s, %s, %s, %s, %s, %s, %s, %s' % (
                    row[0], row[1], row[2] if len(row) > 2 else '', row[3] if len(row) > 3 else '',
                    row[4] if len(row) > 4 else '', row[5] if len(row) > 5 else '',
                    row[6] if len(row) > 6 else '', row[7] if len(row) > 7 else '',
                    row[8] if len(row) > 8 else '', row[9] if len(row) > 9 else ''
                ))
            except IndexError:
                print('Error reading row:', row)

if __name__ == '__main__':
    main()
