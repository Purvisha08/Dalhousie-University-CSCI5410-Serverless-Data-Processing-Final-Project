import gspread
from oauth2client.service_account import ServiceAccountCredentials


# use creds to create a client to interact with the Google Drive API
# scope = ['https://spreadsheets.google.com']
# https://docs.google.com/spreadsheets/d/1ip87WOBNNOTz7-5ggwp-d3BBdQH5kbitv6Ae-2Iwrwo/edit?usp=sharing

def lambda_handler(event, context):
    creds = ServiceAccountCredentials.from_json_keyfile_name('config.json')
    client = gspread.authorize(creds)

    # Find a workbook by name and open the first sheet
    # Make sure you use the right name here.
    sheet = client.open("Data").sheet1

    # Extract and print all of the values
        # list_of_hashes = sheet.get_all_records()
        # print(list_of_hashes)

    return {
        "status": 200,
        "body": "success"
    }
