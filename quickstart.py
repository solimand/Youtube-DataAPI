# Sample Python code for user authorization

import os

import google.oauth2.credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


def channels_list_by_username(service, **kwargs):
    results = service.channels().list(
        **kwargs
    ).execute()

    print('This channel\'s ID is %s. Its title is %s, and it has %s views and %s subscribers.' %
          (results['items'][0]['id'],
           # 'snippet' and 'statistics' have many items inside
           results['items'][0]['snippet']['title'],
           results['items'][0]['statistics']['viewCount'],
           results['items'][0]['statistics']['subscriberCount']))


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print('Usage: %s <Youtube Username>' %sys.argv[0])
        sys.exit("Provide more args, please")

    username = sys.argv[1]

    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '0'
    service = get_authenticated_service()
    channels_list_by_username(service, part='snippet,contentDetails,statistics', forUsername=username)
