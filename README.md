# Python & Youtube API Client
## Prerequisites
We need credentials and an allowed app:
- create or select a project in the **Google Developers Console** 
- select the **OAuth consent screen tab**. Select an Email address, enter a Product name if not already set, and click the Save button
- select the **Credentials** tab, click the **Create credentials** button and select **OAuth client ID**
- select the application type **Other**, enter the name **YouTube Data API Quickstart**, and click the **Create** button
- optionally download the JSON, move it to your working directory and rename it **client_secret.json**. 
Alternatively you can write by-hand your client_secret.json

The sample attempts to open a new window or tab in your default browser. 
If this fails, copy the URL from the console and manually open it in your browser.
If you are not already logged into your Google account, you will be prompted to log in. 
If you are logged into multiple Google accounts, you will be asked to select one account to use for the authorization.

## Quick Start
### Installed App version
The Quickstart example prints some info about a Youtube channel.
Usage: `python quickstart.py <Youtube User Name>`

### Web Server version
Don't need to authenticate every time, but the server remains active with an authenticated session.
Usage: `python quickstart-webapp.py <Youtube User Name>` 

## Youtube Playlist
Providing a _Youtube user name_ and a _Youtube playlist name_ to the module yt-playlist, it gets:
- the channel ID
- the playlist ID
- the name of the videos of the playlist
Usage: `python yt-playlist.py <Youtube User Name> <Youtube Playlist Name>`
The module saves a file with all the song names in the home of the user (platform independently). 

## References
- https://developers.google.com/youtube/v3/quickstart/python
- https://developers.google.com/youtube/v3/docs/playlists
- https://developers.google.com/youtube/v3/docs/playlistItems