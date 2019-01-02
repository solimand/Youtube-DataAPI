# Youtube Python module to extract channel playlists
# TODO requiements file...

import os
import time
from pathlib import Path

# import google.oauth2.credentials
# import google_auth_oauthlib.flow
# from googleapiclient.errors import HttpError

from pathlib import Path
from googleapiclient.discovery import build
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


def print_playlist_items_name(playlist, file):
    for song in playlist['items']:
        # print(song['snippet']['title'])
        file.write(song['snippet']['title']+'\n')


# Build a resource based on a list of properties given as key-value pairs.
# Leave properties with empty values out of the inserted resource.
def build_resource(properties):
    resource = {}
    for p in properties:
        # Given a key like "snippet.title", split into "snippet" and "title", where
        # "snippet" will be an object and "title" will be a property in that object.
        prop_array = p.split('.')
        ref = resource
        for pa in range(0, len(prop_array)):
            is_array = False
            key = prop_array[pa]

            # For properties that have array values, convert a name like
            # "snippet.tags[]" to snippet.tags, and set a flag to handle
            # the value as an array.
            if key[-2:] == '[]':
                key = key[0:len(key) - 2:]
                is_array = True

            if pa == (len(prop_array) - 1):
                # Leave properties without values out of inserted resource.
                if properties[p]:
                    if is_array:
                        ref[key] = properties[p].split(',')
                    else:
                        ref[key] = properties[p]
            elif key not in ref:
                # For example, the property is "snippet.title", but the resource does
                # not yet have a "snippet" object. Create the snippet object here.
                # Setting "ref = ref[key]" means that in the next time through the
                # "for pa in range ..." loop, we will be setting a property in the
                # resource's "snippet" object.
                ref[key] = {}
                ref = ref[key]
            else:
                # For example, the property is "snippet.description", and the resource
                # already has a "snippet" object.
                ref = ref[key]
    return resource


# Remove keyword arguments that are not set
def remove_empty_kwargs(**kwargs):
    good_kwargs = {}
    if kwargs is not None:
        # for key, value in kwargs.iteritems():
        for key, value in kwargs.items():
            if value:
                good_kwargs[key] = value
    return good_kwargs


# Utils method
def channelID_by_username(service, **kwargs):
    results = service.channels().list(
        **kwargs
    ).execute()

    # TEST
    # print('This channel\'s ID is %s. Its title is %s, and it has %s views and %s subscribers.' %
    #      (results['items'][0]['id'],
    #       # 'snippet' and 'statistics' have many items inside
    #       results['items'][0]['snippet']['title'],
    #       results['items'][0]['statistics']['viewCount'],
    #       results['items'][0]['statistics']['subscriberCount']))

    channelID=results['items'][0]['id']
    print('This channel\'s ID is %s.' % channelID)
    return channelID


# Utils method
def playlistID_by_playlistName(client, playlistName, **kwargs):
    kwargs = remove_empty_kwargs(**kwargs)

    response = client.playlists().list(
        **kwargs
    ).execute()

    playlistCount = response['items'].__len__()
    print("Channel have %d playlists" % playlistCount)

    for tmp in response['items']:
        print(tmp['snippet']['title'])
        if playlistName==tmp['snippet']['title']:
            videoCount=tmp['contentDetails']['itemCount']
            playlistID=tmp['id']
            print('Playlist %s have %d videos and ID = %s' %(playlistName, videoCount, playlistID))
    return playlistID


# Utils method
def playlist_items_list_by_playlist_id(client, playlistName, **kwargs):
    kwargs = remove_empty_kwargs(**kwargs)

    response = client.playlistItems().list(
        **kwargs
    ).execute()

    # playlist name could hava chars not allowed in file name...
    # path is platform independent
    file_name=('yt-playlist'+time.strftime("%Y%m%d")+'.txt')
    path_to_file = Path.home() / file_name
    video_names_file = open(path_to_file, 'w')

    while True:
        print_playlist_items_name(response, video_names_file)

        try:
            next_page_token = response['nextPageToken']
            print('Another page yet...')
        except KeyError:
            print("Last page reached or one-page result.")
            break

        response = client.playlistItems().list(
            **kwargs,
            pageToken=next_page_token
        ).execute()

    video_names_file.close()


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 3:
        print('Usage: %s <Youtube User Name> <Youtube Playlist Name>' % sys.argv[0])
        sys.exit("Provide more args, please")

    username = sys.argv[1]
    playlistName = sys.argv[2]

    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '0'
    client = get_authenticated_service()

    channelID=channelID_by_username(client, part='snippet,contentDetails,statistics',
                                    forUsername=username)

    playlistsID=playlistID_by_playlistName(client, playlistName,
                                           part='snippet,contentDetails',
                                           channelId=channelID,
                                           maxResults=50)

    playlist_items_list_by_playlist_id(client, playlistName,
                                      part='snippet,contentDetails',
                                      maxResults=50,
                                      playlistId=playlistsID)

    print("End of Program")
    sys.exit(0)
