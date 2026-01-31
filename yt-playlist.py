"""
Export ALL playlists and their tracks from a YouTube account.
Creates one .txt file per playlist.
"""

import os
import pickle
import re
import unicodedata

from pathlib import Path
from typing import List, Dict

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
# from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

# ==============================
# CONFIG
# ==============================

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
OUTPUT_DIR = Path.home() / "youtube_playlists"
TOKEN_FILE = "token.pickle"

# ==============================
# AUTH
# ==============================

def get_service():
    creds = None

    # Load saved credentials
    if Path(TOKEN_FILE).exists():
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    # If no valid creds → login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            secret_file = choose_client_secret_file()
            flow = InstalledAppFlow.from_client_secrets_file(secret_file, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save credentials for next run
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    return build("youtube", "v3", credentials=creds)

# ==============================
# API HELPERS
# ==============================

def paginate(list_next, request):
    while request:
        response = request.execute()
        yield response
        request = list_next(request, response)


def get_channel_id(service, username: str) -> str:
    response = service.channels().list(
        part="id",
        forUsername=username
    ).execute()

    return response["items"][0]["id"]


def get_all_playlists(service, channel_id: str) -> List[Dict]:
    playlists = []

    request = service.playlists().list(
        part="snippet,contentDetails",
        channelId=channel_id,
        maxResults=50
    )

    for page in paginate(service.playlists().list_next, request):
        playlists.extend(page["items"])

    return playlists


def get_playlist_tracks(service, playlist_id: str) -> List[str]:
    titles = []

    request = service.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    )

    for page in paginate(service.playlistItems().list_next, request):
        for item in page["items"]:
            titles.append(item["snippet"]["title"])

    return titles


# ==============================
# FILE IO
# ==============================

def save_playlist(name: str, tracks: List[str]):
    """Save playlist tracks to a safe filename, overwriting if it exists."""
    OUTPUT_DIR.mkdir(exist_ok=True)

    safe_name = normalize_filename(name)

    path = OUTPUT_DIR / f"{safe_name}.txt"

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(tracks))

    print(f"Saved {len(tracks)} tracks → {path}")

def normalize_filename(name: str) -> str:
    """Convert playlist title into safe filename.
        - remove accents/emoji → ascii
        - lowercase
        - replace non-alphanumeric with dash
        - collapse multiple dashes
        - trim edges
        - fallback if empty (e.g. "!!!")
    """
    name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    name = name.lower()
    name = re.sub(r"[^a-z0-9]+", "-", name)
    name = re.sub(r"-+", "-", name)
    name = name.strip("-")
    return name or "playlist"

# ==============================
# Choose client secret
# ==============================

def choose_client_secret_file() -> Path:
    """Search current folder for client_secret files and let user pick one."""

    files = sorted(Path(".").glob("*client_secret*"))

    if not files:
        raise FileNotFoundError(
            "No files containing 'client_secret' found in current directory."
        )

    # only one → auto select
    if len(files) == 1:
        print(f"Using client secret: {files[0].name}")
        return files[0]

    # multiple → ask user
    print("\nAvailable client secret files:\n")

    for i, f in enumerate(files, 1):
        print(f"{i}) {f.name}")

    while True:
        choice = input("\nSelect file number: ")

        if choice.isdigit() and 1 <= int(choice) <= len(files):
            selected = files[int(choice) - 1]
            print(f"Using: {selected.name}\n")
            return selected

        print("Invalid selection. Try again.")

# ==============================
# MAIN
# ==============================

def main(username: str):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

    service = get_service()
    channel_id = get_channel_id(service, username)

    playlists = get_all_playlists(service, channel_id)

    print(f"Found {len(playlists)} playlists\n")

    for playlist in playlists:
        name = playlist["snippet"]["title"]
        pid = playlist["id"]

        print(f"Fetching: {name}")
        tracks = get_playlist_tracks(service, pid)

        save_playlist(name, tracks)


if __name__ == "__main__":
    import sys

    script_name = Path(__file__).name

    if len(sys.argv) != 2:

        print(f"Usage: python {script_name} <username>")
        sys.exit(1)

    main(sys.argv[1])
