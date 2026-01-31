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

---

## Local Env

- create a python virtual env `python3 -m venv ./venv`
- activate it `. venv/bin/activate.fish` (fish shell)
- install requirements `pip install -r requirements.txt`

---

## AUTH

On first run:

- Browser opens
- Google login page appears
- You grant permission
- Token is saved locally

After that:

- No browser opens
- Script runs silently

### How authentication works

1. Script loads saved token if available
2. If missing/expired → opens browser login
3. Google returns OAuth token
4. Token is saved
5. API requests use that token automatically

---

## Generated Files

`token.pickle` -> Saved login credentials (so you don't re-login each run)

`youtube_playlists/` -> One .txt file per playlist

## Youtube Playlist

Providing a _Youtube user name_ and a _Youtube playlist name_ to the module yt-playlist, it gets:

- the channel ID
- the playlist ID
- the name of the videos of the playlist
Usage: `python yt-playlist.py <Youtube User Name>`
The module saves a file with all the song names in the home of the user (platform independently).

## Quick Start

### Installed App version WIP

The Quickstart example prints some info about a Youtube channel.
Usage: `python quickstart.py <Youtube User Name>`

### Web Server version WIP

Don't need to authenticate every time, but the server remains active with an authenticated session.
Usage: `python quickstart-webapp.py <Youtube User Name>`

## References

- <https://developers.google.com/youtube/v3/quickstart/python>
- <https://developers.google.com/youtube/v3/docs/playlists>
- <https://developers.google.com/youtube/v3/docs/playlistItems>
